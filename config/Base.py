from config.Path import *
from utils.DBUtils import *
from utils.LogUtil import Log
import subprocess

log = Log.logger


# 1、定义init_db
def init_db(db_alia):

    # 2、初始化数据信息，通过配置
    db_info = ConfigYaml().get_db_conf_info(db_alia)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    db_name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])

    # 3、初始化mysql对象
    conn = Mssql(host,user,password,db_name,charset,port)
    print(conn)
    return conn


def allure_report(report_path,report_html):
    """
    生成allure报告
    :param report_path:
    :param report_html:
    :return:
    """
    # 执行命令 allure generate
    allure_cmd = "allure generate %s -o %s --clean"%(report_path,report_html)
    print(allure_cmd)
    # subprocess.call
    log.info("测试报告地址")
    try:
        subprocess.call(allure_cmd,shell=True)
    except:
        log.error("执行用例失败，请检查一下测试环境相关配置")
        raise


if __name__ == "__main__":
    init_db("db_1")