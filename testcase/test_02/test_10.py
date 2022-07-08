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


@allure.feature("互联网+业务总量")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getBusinessJhDbTotal.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("业务总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '业务总量')
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

        api_res = r['body']['data']['ywlxDetailDtos']['zl'][0]
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 数据库业务总量
        sql = "SELECT substring(ywh,0,4),count(DISTINCT YWH)  FROM ESTATE_QLXX WHERE REGISTED = 1 AND	QSZT BETWEEN 1 AND 2 AND DJSJ   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' GROUP BY substring(ywh,0,4)"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        global zl
        zl = 0
        if len(db_res) > 0:
            for item in db_res:
                zl += item[1]
                print(item)

        # 总量
        api_zl = api_res['zl']
        print(api_zl)

        try:
            assert int(zl) == int(api_zl)
            return True
        except:
            log.error("业务总量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("业务总量数据库查询结果： %s" % zl + "，接口返回结果：%s" % api_zl + "\n")
            raise

    @allure.story("产权首次登记业务总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '产权首次登记业务总量')
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

        api_res = r['body']['data']['ywlxDetailDtos']['sc'][0]
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 产权首次登记业务总量
        sql = "SELECT substring(ywh,0,4),count(DISTINCT YWH)  FROM ESTATE_QLXX WHERE REGISTED = 1 AND	QSZT BETWEEN 1 AND 2 AND DJSJ   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'and DJDL = '100' and DJLX like '01%' GROUP BY substring(ywh,0,4)"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        global zl
        zl = 0
        if len(db_res) > 0:
            for item in db_res:
                zl += item[1]
                print(item)

        # 总量
        api_zl = api_res['zl']
        print(api_zl)

        try:
            assert int(zl) == int(api_zl)
            return True
        except:
            log.error("产权首次登记业务总量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("产权首次登记业务总量数据库查询结果： %s" % zl + "，接口返回结果：%s" % api_zl + "\n")
            raise

    @allure.story("产权转移登记业务总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '产权转移登记业务总量')
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

        api_res = r['body']['data']['ywlxDetailDtos']['zy'][0]
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 产权转移登记业务总量
        sql = "SELECT substring(ywh,0,4),count(DISTINCT YWH)  FROM ESTATE_QLXX WHERE REGISTED = 1 AND	QSZT BETWEEN 1 AND 2 AND DJSJ   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'and DJDL = '200' and DJLX like '01%' GROUP BY substring(ywh,0,4)"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        global zl
        zl = 0
        if len(db_res) > 0:
            for item in db_res:
                zl += item[1]
                print(item)

        # 总量
        api_zl = api_res['zl']
        print(api_zl)

        try:
            assert int(zl) == int(api_zl)
            return True
        except:
            log.error("产权转移登记业务总量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("产权转移登记业务总量数据库查询结果： %s" % zl + "，接口返回结果：%s" % api_zl + "\n")
            raise

    @allure.story("抵押登记业务量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_04(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '抵押登记业务量')
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

        api_res = r['body']['data']['ywlxDetailDtos']['dy'][0]
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 抵押登记业务量
        sql = "SELECT substring(ywh,0,4),count(DISTINCT YWH)  FROM ESTATE_QLXX WHERE REGISTED = 1 AND	QSZT BETWEEN 1 AND 2 AND DJSJ   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and DJLX like '03%' GROUP BY  substring(DJLX,0,3),substring(ywh,0,4)	"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        global zl
        zl = 0
        if len(db_res) > 0:
            for item in db_res:
                zl += item[1]
                print(item)

        # 总量
        api_zl = api_res['zl']
        print(api_zl)

        try:
            assert int(zl) == int(api_zl)
            return True
        except:
            log.error("抵押登记业务量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("抵押登记业务量数据库查询结果： %s" % zl + "，接口返回结果：%s" % api_zl + "\n")
            raise

    @allure.story("预告登记业务量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_05(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '预告登记业务量')
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

        api_res = r['body']['data']['ywlxDetailDtos']['yg'][0]
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 预告登记业务量
        sql = "SELECT substring(ywh,0,4),count(DISTINCT YWH)  FROM ESTATE_QLXX WHERE REGISTED = 1 AND	QSZT BETWEEN 1 AND 2 AND DJSJ   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and DJLX like '02%' GROUP BY  substring(DJLX,0,3),substring(ywh,0,4)"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        global zl
        zl = 0
        if len(db_res) > 0:
            for item in db_res:
                zl += item[1]
                print(item)

        # 总量
        api_zl = api_res['zl']
        print(api_zl)

        try:
            assert int(zl) == int(api_zl)
            return True
        except:
            log.error("预告登记业务量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("预告登记业务量数据库查询结果： %s" % zl + "，接口返回结果：%s" % api_zl + "\n")
            raise
