import os
import shutil
import time
import click
import pytest
from utils.LogUtil import *
from config.Conf import RunConfig, PathConfig
from utils.ReportUtil import Report
from utils.SendWxUtil import send_wx
from testcase import globalVar

'''
说明：
1、用例创建原则，测试文件名必须以“test”开头，测试类必须以“Test”开头，测试函数必须以“test”开头。
2、运行方式：
  > python run.py  (回归模式，生成HTML报告)
  > python run.py -t debug  (调试模式)
  > python run.py -c 要执行的用例 (默认读取配置文件的，自定义用例时使用)
  > python run.py -m 标签名 （执行指定标签的用例，默认按照配置文件的用例搜索）
'''
logger = Log.logger
def init_dir():
    """初始化测试报告目录，按照配置保留最大报告数"""
    global result_dir, allure_report, xml_report
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    files = os.listdir(PathConfig.report)
    files.sort()
    if len(files) > int(RunConfig.report_number_max):
        path_list = [os.path.join(PathConfig.report, i) for i in files]
        for i in range(len(path_list) - int(RunConfig.report_number_max)):
            logger.info(f'删除目录：{path_list[i]}')
            # 验证下是否是文件夹
            if os.path.isdir(path_list[i]):
                shutil.rmtree(path_list[i])
    result_dir = os.path.join(PathConfig.report, now_time, 'allure_result')  # 存放allure结果目录
    allure_report = os.path.join(PathConfig.report, now_time, 'allure_report')  # 存放allure报告地址
    xml_report = os.path.join(PathConfig.report, now_time, "junit-xml.xml")  # 存放生成的xml文件地址
    logger.info(f'创建目录：{result_dir}，{allure_report}')
    os.makedirs(result_dir)
    os.makedirs(allure_report)
    logger.info("初始化报告目录完成")


# @click.command()
# @click.option('-t', default=None, help='输入运行模式：run 或 debug.')
# @click.option('-c', default=None, help='要执行的用例集')
# @click.option('-m', default=None, help='要执行用例的标签')
def run(t, c, m):
    if t is None or t == "run":
        logger.info("回归模式，开始执行")
        init_dir()
        # 获取用例集
        if c:
            test_cases = c
        else:
            test_cases = RunConfig.cases_path
        py_list = ["-s", "-v", test_cases,
                   "--junit-xml=" + xml_report,
                   "--alluredir=" + result_dir,
                   "--maxfail", RunConfig.max_fail,
                   "--reruns", RunConfig.rerun]
        if m:
            # 存在标签，按标签执行
            py_list.insert(2, "-m")
            py_list.insert(3, m)
        pytest.main(py_list)
        logger.info("用例执行结束，开始生成测试报告！")
        Report.add_env(result_dir)
        if RunConfig.exe_mode == 'local':
            general_report()
            logger.info('allure报告生成完成')
        if RunConfig.send_wx_message:
            send_wx(xml_report, RunConfig.test_env_config)
            logger.info("企业微信通知已发送")
    elif t == "debug":
        print("debug模式，开始执行！")
        pytest.main(["-v", "-s", RunConfig.cases_path])
    logger.info("运行结束！！")

def general_report():
    report = Report()
    cmd = "{} generate {} -o {} --clean".format(report.allure, result_dir, allure_report)
    logger.info(os.popen(cmd).read())

if __name__ == '__main__':
    globalVar._init()
    # run()
    run('run','','dxts')