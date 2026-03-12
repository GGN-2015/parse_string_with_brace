import sys
sys.setrecursionlimit(5000) # 设置最大递归深度

import os
import json
from . import FileRunner, get_version

# 从命令行中拆分出所有 -I 命令处理
def split_include_path(argv_list:list[str]) -> tuple[list[str], list[str]]:
    CMD_PREFIX = "-I"
    index = 0
    new_argv_list = []     # 删除 -I 命令后的其他命令
    include_path_list = [] # 拆分出所有 include_path
    while index < len(argv_list):

        # 检测到了 -I 的命令
        if argv_list[index].startswith(CMD_PREFIX):

            # 单纯的 -I 命令：下一个对象将会是路径描述符
            if len(argv_list[index]) == len(CMD_PREFIX):
                if (index + 1) >= len(argv_list):
                    raise ValueError("\"-I\" should be followed by a path.")
                include_path_list.append(argv_list[index + 1].strip())
                index += 2

            # 自身带有路径的 -I 命令
            else:
                if len(argv_list[index]) <= len(CMD_PREFIX): # 一定更长
                    raise AssertionError()
                other_part = argv_list[index][len(CMD_PREFIX):] # 删除前缀
                include_path_list.append(other_part.strip())
                index += 1
        
        # 检测到了无关命令
        else: 
            new_argv_list.append(argv_list[index])
            index += 1
    
    # 返回拆分后的结果
    # 注意 "-I." 以及 "-I.." 之类的写法需要改写成当前工作目录相对路径
    return new_argv_list, [
        os.path.abspath(os.getcwd()) if include_path == "." else (
        os.path.dirname(os.path.abspath(os.getcwd())) if include_path == ".." else include_path)
        for include_path in include_path_list
    ]

# 检查某个字符串是否存在
# 并返回删除该字符串后的结果
def check_and_erase(argv_list:list[str], aim_str:str) -> tuple[list[str], bool]:
    ans = aim_str in argv_list
    new_argv_list = [
        item
        for item in argv_list
        if item != aim_str
    ]
    return new_argv_list, ans

def main(argv_list:list[str]) -> int:

    # 检查 -I 命令
    # 这个命令用于指定 include 路径
    try:
        argv_list, inlcude_path_list = split_include_path(argv_list)
    except ValueError as e:
        print("<CMD:1>", e)
        return 1

    # 检查 --verbose：是否需要逐条输出匹配过程
    argv_list, verbose = check_and_erase(argv_list, "--verbose")
    argv_list, step_mode = check_and_erase(argv_list, "--step")

    # --step 的功能，是在开启 --verbose 的前提下
    # 每次替换后，需要按一下 Enter 才能继续执行，方便观察代码运行是否正确
    if step_mode == True and verbose == False:
        print("<CMD>:1", "\"--step\" can only work with \"--verbose\".")
        return 1

    # 初始化文件运行器
    try:
        file_runner = FileRunner(inlcude_path_list)
        file_runner.verbose = verbose
        file_runner.step_mode = step_mode

    # 在初始化过程中如果出现错误
    # 一般来说是 -I 指定的 include_path 不存在
    except Exception as e:
        print("<CMD>:1", e)
        return 1

    # 参数中没有指定需要运行的文件
    # 启动交互式命令行
    if argv_list == []:
        print(f"xulang interactive command line v{get_version()}")
        file_runner.interactive_ui()

    # 检查命令行中指定的文件个数是否超过一个
    # 如果超过一个，则报错，并显示帮助信息
    elif len(argv_list) > 1:
        print("Usage:")
        print("    python3 -m xulang")
        print("    python3 -m xulang <source_file>")
        print("    python3 -m xulang -I <include_path>")
        print("    python3 -m xulang --verbose")
        print("    python3 -m xulang --verbose --step")
        return 1

    # 命令中恰好指定了一个需要执行的文件时
    # 执行这个文件
    else:
        # 检查需要执行的文件是否存在
        filepath = argv_list[0]
        if not os.path.isfile(filepath):
            print(f"<CMD>:1 File \"{filepath}\" not found!")
            return 1
        
        # file_runner.run_file 需要使用绝对路径调用程序
        # 需要将非绝对路径转换为绝对路径
        if not os.path.isabs(filepath): 
            filepath = os.path.abspath(filepath)
        file_runner.run_file(filepath)

    # 返回 0 表示程序自正确结束
    return 0

# 运行主程序
sys.exit(main(json.loads(json.dumps(sys.argv[1:]))))
