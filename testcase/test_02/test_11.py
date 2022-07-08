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

@allure.feature("接口统计")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getInterfaceTotal.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("税务")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '税务')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='税务' and request='获取' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            swhq = db_res[0][2]
        else:
            swhq = 0

        api_swhq = api_res['swhq']

        # 数据库
        sql1 = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='税务' and request='推送' GROUP BY DEPARTMENT,REQUEST"
        db_res1 = DBConfig().dbconfig(sql1)
        print(db_res1)
        if len(db_res1) > 0:
            swts = db_res1[0][2]
        else:
            swts = 0

        api_swts = api_res['swts']

        try:
            assert int(swhq) == int(api_swhq) and int(swts) == int(api_swts)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(swhq) != int(api_swhq):
                log.info("税务获取数据库查询结果： %s" % swhq + "，接口返回结果：%s" % api_swhq + "\n")
            if int(swts) != int(api_swts):
                log.info("税务推送数据库查询结果： %s" % swts + "，接口返回结果：%s" % api_swts + "\n")
            raise

    @allure.story("住建")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '住建')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='住建' and request='获取' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            zjhq = db_res[0][2]
        else:
            zjhq = 0

        api_zjhq = api_res['zjhq']

        # 数据库
        sql1 = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='住建' and request='推送' GROUP BY DEPARTMENT,REQUEST"
        db_res1 = DBConfig().dbconfig(sql1)
        print(db_res1)
        if len(db_res1) > 0:
            zjts = db_res1[0][2]
        else:
            zjts = 0

        api_zjts = api_res['zjts']

        try:
            assert int(zjhq) == int(api_zjhq) and int(zjts) == int(api_zjts)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(zjhq) != int(api_zjhq):
                log.info("住建获取数据库查询结果： %s" % zjhq + "，接口返回结果：%s" % api_zjhq + "\n")
            if int(zjts) != int(api_zjts):
                log.info("住建推送数据库查询结果： %s" % zjts + "，接口返回结果：%s" % api_zjts + "\n")
            raise

    @allure.story("公安")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '公安')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='公安' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            ga = db_res[0][2]
        else:
            ga = 0

        api_ga = api_res['ga']


        try:
            assert int(ga) == int(api_ga)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(ga) != int(api_ga):
                log.info("公安数据库查询结果： %s" % ga + "，接口返回结果：%s" % api_ga + "\n")
            raise

    @allure.story("民政")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_04(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '民政')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='民政' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            mz = db_res[0][2]
        else:
            mz = 0

        api_mz = api_res['mz']


        try:
            assert int(mz) == int(api_mz)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(mz) != int(api_mz):
                log.info("民政数据库查询结果： %s" % mz + "，接口返回结果：%s" % api_mz + "\n")
            raise

    @allure.story("市场监管")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_05(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '市场监管')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='市场监管' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            scjg = db_res[0][2]
        else:
            scjg = 0

        api_scjg = api_res['scjg']


        try:
            assert int(scjg) == int(api_scjg)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(scjg) != int(api_scjg):
                log.info("市场监管数据库查询结果： %s" % scjg + "，接口返回结果：%s" % api_scjg + "\n")
            raise

    @allure.story("编办")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_06(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '编办')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='编办' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            bb = db_res[0][2]
        else:
            bb = 0

        api_bb = api_res['bb']


        try:
            assert int(bb) == int(api_bb)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(bb) != int(api_bb):
                log.info("编办数据库查询结果： %s" % bb + "，接口返回结果：%s" % api_bb + "\n")
            raise

    @allure.story("卫健委")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_07(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '卫健委')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='卫健委' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            wjw = db_res[0][2]
        else:
            wjw = 0

        api_wjw = api_res['wjw']


        try:
            assert int(wjw) == int(api_wjw)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(wjw) != int(api_wjw):
                log.info("卫健委数据库查询结果： %s" % wjw + "，接口返回结果：%s" % api_wjw + "\n")
            raise

    @allure.story("发改委")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_08(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '发改委')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='发改委' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            fgw = db_res[0][2]
        else:
            fgw = 0

        api_fgw = api_res['fgw']


        try:
            assert int(fgw) == int(api_fgw)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(fgw) != int(api_fgw):
                log.info("发改委数据库查询结果： %s" % fgw + "，接口返回结果：%s" % api_fgw + "\n")
            raise

    @allure.story("国家电网")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_09(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '国家电网')
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

        # 数据库
        sql = " SELECT  DEPARTMENT department,REQUEST request,COUNT (DEPARTMENT) num FROM ESTATE_RECORD_DSF WHERE  DATE_TIME   BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' and department='国家电网' GROUP BY DEPARTMENT,REQUEST"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            gjdw = db_res[0][2]
        else:
            gjdw = 0

        api_gjdw = api_res['gjdw']


        try:
            assert int(gjdw) == int(api_gjdw)
            return True
        except:
            log.error("接口统计查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(gjdw) != int(api_gjdw):
                log.info("国家电网数据库查询结果： %s" % gjdw + "，接口返回结果：%s" % api_gjdw + "\n")
            raise


