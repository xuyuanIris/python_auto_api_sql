import os
from utils.YamlUtil import *

# 获取项目根本路径
# 获取当前项目的绝对路径
current = os.path.abspath(__file__)
# print(current)
BASE_DIR = os.path.dirname(os.path.dirname(current))
# print(BASE_DIR)
# 定义config目录路径
_config_path = BASE_DIR + os.sep + "config"
# 定义data目录路径
_data_path = BASE_DIR + os.sep + "data"
# 定义testcase目录路径
_testcase_path = BASE_DIR + os.sep + "testcase/"
# 定义conf.yaml文件路径
_config_file = _config_path + os.sep + "conf.yaml"
# 定义db_conf.yaml文件路径
_db_config_file = _config_path + os.sep + "db_conf.yaml"
# 定义log文件路径
_log_path =  BASE_DIR + os.sep + "logs"
# 定义report文件路径
_report_path =  BASE_DIR + os.sep + "report"


def get_testcase_path():
    """
    获取testcase绝对路径
    :return:
    """
    return _testcase_path


def get_report_path():
    """
    获取report绝对路径
    :return:
    """
    return _report_path


def get_data_path():
    """
    获取data绝对路径
    :return:
    """
    return _data_path


def get_db_config_file():
    """
    获取db绝对路径
    :return:
    """
    return _db_config_file


def get_config_path():
    """
    获取config绝对路径
    :return:
    """
    return _config_path


def get_config_file():
    """
    获取yaml文件路径
    :return:
    """
    return _config_file


def get_log_path():
    """
    获取log文件路径
    :return:
    """
    return _log_path


# 读取配置文件
class ConfigYaml:

    # 初始化yaml读取配置文件
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()

    # 定义方法获取需要的信息
    def get_conf_url(self):
        """
        获取需要的信息
        :return:
        """
        return self.config["BASE"]["test"]["url"]

    def get_conf_log(self):
        """
        获取日志级别
        :return:
        """
        return self.config['BASE']['log_level']

    def get_conf_log_extension(self):
        """
        获取扩展名
        :return:
        """
        return self.config['BASE']['log_extension']

    def get_db_conf_info(self,db_alias):
        """
        根据db_alias获取该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.db_config[db_alias]


if __name__ == "__main__":
    conf_read = ConfigYaml()
    print(conf_read.get_conf_url())
    # print(conf_read.get_conf_log())
    # print(conf_read.get_conf_log_extension())
    # print(conf_read.get_db_conf_info("db_1"))
# 初始化数据库信息，Base.py init_db
# 接口用例返回结果内容进数据哭验证

