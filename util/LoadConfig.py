import os
import sys
import yaml
home_dir = os.path.dirname(os.getcwd())
print(home_dir)
sys.path.append(home_dir)

def get_conf(project: str) -> dict:
    """
    :param project: 配置项目
    :return: 对应字典
    """
    with open("../config/config.yml", "r") as f:
        yml = yaml.load(f.read(), Loader=yaml.Loader)
        conf = yml[project]
    return conf


if __name__ == "__main__":

    get_conf('mysql')
