import functools
import pip_pkg_info

@functools.cache
def get_version_in_toml() -> str:
    import os
    DIRNOW = os.path.dirname(os.path.abspath(__file__))
    TOML_PATH = os.path.join(DIRNOW, "..", "pyproject.toml")

    if not os.path.isfile(TOML_PATH):
        return "unknown"

    for line in open(TOML_PATH):
        line = line.strip()
        if line.find("version") != -1: # 找到 version
            if line[-1] == "\"":
                return line[1:-1].split("\"")[-1]
    
    return "unknown"

# 获得当前软件的版本
@functools.cache
def get_version(pkg_name_now:str="xulang") -> str:
    dic = pip_pkg_info.pip_pkg_info()

    if dic.get(pkg_name_now) is not None:
        return dic[pkg_name_now]["version"]
    
    else:
        return get_version_in_toml()

if __name__ == "__main__":
    print(get_version())
