import sys
import os
import json
from . import FileRunner, get_version

def main(argv_list:list[str]) -> int:
    file_runner = FileRunner()

    if argv_list == []: # 启动交互式命令行
        print(f"xulang interactive command line v{get_version()}")
        file_runner.interactive_ui()

    else:
        if len(argv_list) > 1:
            print("Usage:")
            print("    python3 -m xulang")
            print("    python3 -m xulang <source_file>")
            return 1

        filepath = argv_list[0]
        if not os.path.isfile(filepath):
            print(f"File \"{filepath}\" not found!")
            return 1
        file_runner.run_file(filepath)

    return 0

# 运行主程序
sys.exit(main(json.loads(json.dumps(sys.argv[1:]))))
