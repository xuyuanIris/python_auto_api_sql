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


@allure.feature("大厅窗口查档量")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getWindowSearchInfo.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()


    @allure.story("批量权利人查询")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"]+"批量权利人查询")
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

        # 数据库批量权利人查询
        sql_plqlr = "SELECT COUNT(SJ) TOTAL, CAST( SUM(CXSL)  as int) PERSON_TOTAL  FROM (SELECT CONVERT(VARCHAR(100), CXSJ, 23) SJ, CXSL FROM ESTATE_EXT_CX_CDZM WHERE ZT IN ('1', '2') AND CXSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000') TEMP  "
        db_plqlr = DBConfig().dbconfig(sql_plqlr)
        print(db_plqlr)
        if len(db_plqlr) > 0:
            db_plqlrTotal = db_plqlr[0][0]
            if db_plqlrTotal is None:
                db_plqlrTotal = 0
            db_plqlrPersonTotal = db_plqlr[0][1]
            if db_plqlrPersonTotal is None:
                db_plqlrPersonTotal = 0
        else:
            db_plqlrTotal = 0
            db_plqlrPersonTotal = 0
        # 接口返回
        api_plqlrTotal = api_res['plqlrTotal']
        print(api_plqlrTotal)
        api_plqlrPersonTotal = api_res['plqlrPersonTotal']
        print(api_plqlrPersonTotal)

        try:
            assert int(db_plqlrTotal) == int(api_plqlrTotal) and int(db_plqlrPersonTotal) == int(api_plqlrPersonTotal)
            return True
        except:
            log.error("批量权利人查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(db_plqlrTotal) != int(api_plqlrTotal):
                log.info("批量权利人次数据库查询结果： %s" % db_plqlrTotal + "，接口返回结果：%s" % api_plqlrTotal + "\n")
            if int(db_plqlrPersonTotal) != int(api_plqlrPersonTotal):
                log.info("批量权利人查询次/人数据库查询结果： %s" % db_plqlrPersonTotal + "，接口返回结果：%s" % api_plqlrPersonTotal + "\n")
            raise


    @allure.story("批量抵押物查询")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"]+"批量抵押物查询")
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

        # 数据库批量抵押物查询
        sql_pldyw = "SELECT COUNT(SJ) TOTAL, CAST( SUM(CXSL)  as int)  PERSON_TOTAL FROM ( SELECT CONVERT(VARCHAR(100), CXSJ, 23) SJ, CXSL FROM ESTATE_EXT_DYCX_INFO WHERE ZT = '1' AND CXSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000') TEMP  "
        db_pldyw = DBConfig().dbconfig(sql_pldyw)
        print(db_pldyw)
        if len(db_pldyw) > 0:
            db_pldywTotal = db_pldyw[0][0]
            if db_pldywTotal is None:
                db_pldywTotal = 0
            db_pldywPersonTotal = db_pldyw[0][1]
            if db_pldywPersonTotal is None:
                db_pldywPersonTotal = 0
        else:
            db_pldywTotal = 0
            db_pldywPersonTotal = 0
        # 接口返回
        api_pldywTotal = api_res['pldywTotal']
        print(api_pldywTotal)
        api_pldywPersonTotal = api_res['pldywPersonTotal']
        print(api_pldywPersonTotal)

        try:
            assert int(db_pldywTotal) == int(api_pldywTotal) and int(db_pldywPersonTotal) == int(api_pldywPersonTotal)
            return True
        except:
            log.error("批量抵押物查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(db_pldywTotal) != int(api_pldywTotal):
                log.info("批量抵押物查询次数据库查询结果： %s" % db_pldywTotal + "，接口返回结果：%s" % api_pldywTotal + "\n")
            if int(db_pldywPersonTotal) != int(api_pldywPersonTotal):
                log.info("批量抵押物查询次/人数据库查询结果： %s" % db_pldywPersonTotal + "，接口返回结果：%s" % api_pldywPersonTotal + "\n")
            raise


    @allure.story("家庭组信息查询")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"]+"家庭组信息查询")
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

        # 数据库批量抵押物查询
        sql_famliy = "SELECT  COUNT(SJ) TOTAL FROM (SELECT CONVERT(VARCHAR(100), CXSJ, 23) SJ FROM ESTATE_CHECK_HOUSE_RECORD WHERE CXSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) TEMP"
        if len(DBConfig().dbconfig(sql_famliy)) > 0:
            db_famliy = DBConfig().dbconfig(sql_famliy)[0][0]
        else:
            db_famliy = 0
        print(db_famliy)

        # 接口返回
        api_famliyTdSearchTotal = api_res['famliyTdSearchTotal']
        print(api_famliyTdSearchTotal)
        api_famliyFwSearchTotal = api_res['famliyFwSearchTotal']
        print(api_famliyFwSearchTotal)

        api_famliy = int(api_famliyTdSearchTotal) + int(api_famliyFwSearchTotal)
        try:
            assert int(db_famliy) == int(api_famliy)
            return True
        except:
            log.error("家庭组信息查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(db_famliy) != int(api_famliy):
                log.info("家庭组信息查询数据库查询结果： %s" % db_famliy + "，接口返回结果：%s" % api_famliy + "\n")

            raise


    @allure.story("查档证明查询")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_04(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"]+"查档证明查询")
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

        # 数据库批量抵押物查询
        sql = "SELECT CXLX,COUNT(1) TOTAL  FROM (SELECT CXLX, CONVERT(VARCHAR(100), CXSJ, 23) SJ FROM ESTATE_EXT_NEW_CDZM WHERE CXSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'   and cxlx like '%查档'     ) TEMP  GROUP BY CXLX"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_fw = db_res[0][1]
            print(db_fw)
            db_td = db_res[2][1]
            print(db_td)
        else:
            db_fw = 0
            db_td = 0

        # 接口返回
        api_fw = api_res['searchFwFileTotal']
        api_td = api_res['searchTdFileTotal']
        try:
            assert int(db_fw) == int(api_fw) and int(db_td) == int(api_td)
            return True
        except:
            log.error("查档证明查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(db_fw) != int(api_fw):
                log.info("查档证明fw查询数据库查询结果： %s" % db_fw + "，接口返回结果：%s" % api_fw + "\n")
            if int(db_td) != int(api_td):
                log.info("查档证明td查询数据库查询结果： %s" % db_td + "，接口返回结果：%s" % api_td + "\n")

            raise


    @allure.story("有房证明量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_05(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"]+"有房证明量")
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

        # 数据库批量抵押物查询
        sql = "SELECT CXLX, COUNT(CXLX) TOTAL  FROM (SELECT CXLX, CONVERT(VARCHAR(100), CXSJ, 23) SJ FROM ESTATE_EXT_NEW_CDZM WHERE CXSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and cxlx = '有房' ) TEMP GROUP BY CXLX"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_fw = db_res[0][1]
        else:
            db_fw = 0

        # 接口返回
        api_fw = api_res['houseFwTotal']
        api_td = api_res['houseTdTotal']
        api_yfw = int(api_fw) + int(api_td)
        try:
            assert int(db_fw) == int(api_yfw)
            return True
        except:
            log.error("有房证明量，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("有房证明量数据库查询结果： %s" % db_fw + "，接口返回结果：%s" % api_yfw + "\n")
            raise


    @allure.story("无房证明量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_06(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"]+"无房证明量")
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

        # 数据库批量抵押物查询
        sql = "SELECT CXLX, COUNT(CXLX) TOTAL  FROM (SELECT CXLX, CONVERT(VARCHAR(100), CXSJ, 23) SJ FROM ESTATE_EXT_NEW_CDZM WHERE CXSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'and cxlx = '无房'  ) TEMP GROUP BY CXLX"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_fw = db_res[0][1]
        else:
            db_fw = 0

        # 接口返回
        api_fw = api_res['noHouseFwTotal']
        api_td = api_res['noHouseTdTotal']
        api_yfw = int(api_fw) + int(api_td)
        try:
            assert int(db_fw) == int(api_yfw)
            return True
        except:
            log.error("无房证明量，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("无房证明量数据库查询结果： %s" % db_fw + "，接口返回结果：%s" % api_yfw + "\n")
            raise




