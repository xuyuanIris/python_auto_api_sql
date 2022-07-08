import pytest
from config import Path
import os
from utils.YamlUtil import YamlReader
from config.Path import ConfigYaml
from utils.RequestsUtil import Request
from utils.AssertUtil import AssertUtil
from config.MarkConf import *
import allure
from testcase import globalVar
from config.DBConfig import DBConfig
from utils.LogUtil import *

pytestmark = pytest.mark.zx
request = Request()
# 统一接口路径
url_path = ConfigYaml().get_conf_url()
# 用例数据文件路径
case_path = Path.get_testcase_path() + "test_02"
log = Log.logger


@allure.feature("电子证照量")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getElectricityCertifyTotal.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("电子证书量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '电子证书量')
        # 获取yaml文件的内容
        url = url_path + data_list["url"]
        params = data_list["request"]["params"]
        params['regionCode'] = globalVar.regionCode
        params['areaCode'] = globalVar.areaCode
        headers = data_list["request"]["headers"]
        headers['Cookie'] = globalVar.cookie
        expectcode = data_list["expect"]["code"]
        r = request.post(url, data=params, headers=headers)

        code = r["code"]
        AssertUtil().assert_code(code, expectcode)

        api_res = r['body']['data']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 数据库电子证书量
        sql_certificateTotal = "SELECT COUNT(BDCQZH) SUM FROM (SELECT DISTINCT X.BDCQZH,X.QLLX, CONVERT(VARCHAR(100), Z.SZSJ, 23) SJ FROM ESTATE_DJ_SZ Z LEFT JOIN ESTATE_QLXX X ON Z.YWH = X.YWH WHERE Z.SZSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'AND Z.SZMC in ('不动产权', '不动产权证', '不动产权证书')  AND X.QLLX IN ('1', '3', '7', '5', '15', '17', '4', '24', '8', '26', '6', '25', '27', '28', '23', '10', '12', '9') ) TEMP "
        if len(DBConfig().dbconfig(sql_certificateTotal)) > 0:
            db_certificateTotal = DBConfig().dbconfig(sql_certificateTotal)[0][0]
        else:
            db_certificateTotal = 0
        print(db_certificateTotal)
        # 接口返回
        api_certificateTotal = api_res['certificateTotal']
        print(api_certificateTotal)

        try:
            assert int(db_certificateTotal) == int(api_certificateTotal)
            return True
        except:
            log.error("抵押登记情况-期内新增查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("电子证书量数量数据库查询结果： %s" % db_certificateTotal + "，接口返回结果：%s" % api_certificateTotal + "\n")
            raise

    @allure.story("电子证明量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '电子证明量')
        # 获取yaml文件的内容
        url = url_path + data_list["url"]
        params = data_list["request"]["params"]
        params['regionCode'] = globalVar.regionCode
        params['areaCode'] = globalVar.areaCode
        headers = data_list["request"]["headers"]
        headers['Cookie'] = globalVar.cookie
        expectcode = data_list["expect"]["code"]
        r = request.post(url, data=params, headers=headers)

        code = r["code"]
        AssertUtil().assert_code(code, expectcode)

        api_res = r['body']['data']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 数据库电子证明量
        sql_certufyTotal = "SELECT  COUNT(BDCQZH) SUM FROM (SELECT DISTINCT X.QLTYPE, CONVERT(VARCHAR(100), Z.SZSJ, 23) SJ, X.BDCQZH FROM ESTATE_DJ_SZ Z LEFT JOIN ESTATE_QLXX X ON Z.SZZH = X.BDCQZH WHERE Z.SZMC IN ('不动产权证明', '不动产证明') AND Z.SZSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'AND QLTYPE IN ('DYIDJ', 'YGMMDJ', 'YGDYQDJ','YYDJ', 'DYADJ')   ) TEMP  "
        if len(DBConfig().dbconfig(sql_certufyTotal)) > 0:
            db_certufyTotal = DBConfig().dbconfig(sql_certufyTotal)[0][0]
        else:
            db_certufyTotal = 0
        print(db_certufyTotal)
        # 接口返回
        api_certufyTotal = api_res['certufyTotal']
        print(api_certufyTotal)

        try:
            assert int(db_certufyTotal) == int(api_certufyTotal)
            return True
        except:
            log.error("抵押登记情况-期内新增查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("电子证明量数据库查询结果： %s" % db_certufyTotal + "，接口返回结果：%s" % api_certufyTotal + "\n")
            raise


