import os
import sys
import shutil
import platform
from config.Conf import PathConfig
from config.Conf import RunConfig
from utils.LogUtil import *
from utils.FileReaderUtil import XMLReader


if platform.system() == "Windows":
    allure_path = os.path.join(PathConfig.lib, 'allure', 'bin')
else:
    # 为了适配OS系统
    allure_path = os.path.join(PathConfig.lib, 'allure-2.13.9', 'bin')
sys.path.append(allure_path)


logger = Log.logger


class Report:
    """报告工具类"""
    @property
    def allure(self):
        if platform.system() == "Windows":
            cmd = os.path.join(allure_path, 'allure.bat')
        else:
            cmd = os.path.join(allure_path, 'allure')
        return cmd

    @staticmethod
    def add_env(allure_result_dir):
        """报告中添加环境数据
        :param allure_result_dir:allure报告结果存储目录
        """
        env_file = os.path.join(PathConfig.lib, 'allure', 'environment.xml')
        report_env_file = os.path.join(allure_result_dir, 'environment.xml')
        shutil.copyfile(env_file, report_env_file)
        logger.info("复制报告环境信息文件完成")
        xml = XMLReader(report_env_file)
        values = xml.find_nodes('parameter/value')
        # 项目名称
        values[0].text = RunConfig.project_name
        # 系统
        values[1].text = f'{platform.uname().system} {platform.uname().version} {platform.uname().processor}'
        # python版本
        values[2].text = platform.python_version()
        # allure版本
        values[3].text = '2.8.16'
        # 测试人员
        values[6].text = ''
        xml.write_xml()
        logger.info("报告环境信息文件修改完成")

