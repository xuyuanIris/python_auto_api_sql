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

@allure.feature("登簿量统计")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getDBBusinessTotal.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()


    @allure.story("首次登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '首次登记总量')
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

        # 数据库首次登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL = '100' and QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_sc = db_res[0][0]
        else:
            db_sc = 0
        # 接口返回
        api_sc = api_res['sc']

        try:
            assert int(db_sc) == int(api_sc)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("首次登记总量数据库查询结果： %s" % db_sc + "，接口返回结果：%s" % api_sc + "\n")
            raise


    @allure.story("转移登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '转移登记总量')
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

        # 数据库转移登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL = '200' and QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_zy = db_res[0][0]
        else:
            db_zy = 0
        # 接口返回
        api_zy = api_res['zy']

        try:
            assert int(db_zy) == int(api_zy)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("移登记总量数据库查询结果： %s" % db_zy + "，接口返回结果：%s" % api_zy + "\n")
            raise


    @allure.story("变更登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '变更登记总量')
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

        # 数据库变更登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL = '300' and  QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_bg = db_res[0][0]
        else:
            db_bg = 0
        # 接口返回
        api_bg = api_res['bg']

        try:
            assert int(db_bg) == int(api_bg)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("变更登记总量数据库查询结果： %s" % db_bg + "，接口返回结果：%s" % api_bg + "\n")
            raise


    @allure.story("注销登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_04(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '注销登记总量')
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

        # 数据库注销登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL = '400' and  QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_zx = db_res[0][0]
        else:
            db_zx = 0
        # 接口返回
        api_zx = api_res['zx']

        try:
            assert int(db_zx) == int(api_zx)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("注销登记总量数据库查询结果： %s" % db_zx + "，接口返回结果：%s" % api_zx + "\n")
            raise


    @allure.story("更正登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_05(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '更正登记总量')
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

        # 数据库更正登记总量
        sql = "select count(*) from ESTATE_QLXX where (DJDL = '500'  or DJLX  = '0405') and  QSZT BETWEEN 1 AND 2 AND DJSJ  BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_gz = db_res[0][0]
        else:
            db_gz = 0
        # 接口返回
        api_gz = api_res['gz']

        try:
            assert int(db_gz) == int(api_gz)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("更正登记总量数据库查询结果： %s" % db_gz + "，接口返回结果：%s" % api_gz + "\n")
            raise


    @allure.story("异议登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_06(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '异议登记总量')
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

        # 数据库异议登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL = '600' and  QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_yy = db_res[0][0]
        else:
            db_yy = 0
        # 接口返回
        api_yy = api_res['yy']

        try:
            assert int(db_yy) == int(api_yy)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("异议登记总量数据库查询结果： %s" % db_yy + "，接口返回结果：%s" % api_yy + "\n")
            raise


    @allure.story("预告登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_07(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '预告登记总量')
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

        # 数据库预告登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL = '700' and  QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_yg = db_res[0][0]
        else:
            db_yg = 0
        # 接口返回
        api_yg = api_res['yg']

        try:
            assert int(db_yg) == int(api_yg)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("预告登记总量数据库查询结果： %s" % db_yg + "，接口返回结果：%s" % api_yg + "\n")
            raise


    @allure.story("查封登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_08(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '查封登记总量')
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

        # 数据库查封登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL = '800' and DJLX != '0405'  and  QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_cf = db_res[0][0]
        else:
            db_cf = 0
        # 接口返回
        api_cf = api_res['cf']

        try:
            assert int(db_cf) == int(api_cf)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("查封登记总量数据库查询结果： %s" % db_cf + "，接口返回结果：%s" % api_cf + "\n")
            raise


    @allure.story("其他登记总量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_09(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '其他登记总量')
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

        # 数据库其他登记总量
        sql = "select count(*) from ESTATE_QLXX where DJDL in ('900', '998')  and  QSZT BETWEEN 1 AND 2 AND DJSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_qt = db_res[0][0]
        else:
            db_qt = 0
        # 接口返回
        api_qt = api_res['qt']

        try:
            assert int(db_qt) == int(api_qt)
            return True
        except:
            log.error("登簿量统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("其他登记总量数据库查询结果： %s" % db_qt + "，接口返回结果：%s" % api_qt + "\n")
            raise

