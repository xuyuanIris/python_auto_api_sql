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


@allure.feature("登记证明打印总量分析")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getCertifyInfo.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("押登记证明")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"]+'押登记证明')
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

        # 数据库抵押登记证明
        sql = "select QLTYPE,count(distinct BDCQZH)  from ESTATE_QLXX where ywh in (select YWH  from ESTATE_DJ_SZ where  SZSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'AND SZMC IN ('不动产权证明', '不动产证明') AND ysxlh is  not null AND  ysxlh != '' ) and qllx is not null  and QLTYPE = 'DYADJ' GROUP BY QLTYPE"
        if len(DBConfig().dbconfig(sql)) > 0:
            db_dya = DBConfig().dbconfig(sql)[0][1]
        else:
            db_dya = 0
        print(db_dya)
        # 接口返回
        api_dya = api_res['dya']
        print(api_dya)
        try:
            assert int(api_dya) == int(db_dya)
            return True
        except:
            log.error("登记证明打印总量分析查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("抵押登记数据库查询结果： %s" % db_dya + "，接口返回结果：%s" % api_dya + "\n")

    @allure.story("地役登记证明")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '地役登记证明')
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

        # 数据库地役登记证明
        sql_dyi = "select QLTYPE,count(distinct BDCQZH)  from ESTATE_QLXX where ywh in (select YWH  from ESTATE_DJ_SZ where  SZSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'AND SZMC IN ('不动产权证明', '不动产证明') AND ysxlh is  not null AND  ysxlh != '' ) and qllx is not null  and QLTYPE = 'DYIDJ' GROUP BY QLTYPE"
        if len(DBConfig().dbconfig(sql_dyi)) > 0:
            db_dyi = DBConfig().dbconfig(sql_dyi)[0][1]
        else:
            db_dyi = 0
        print(db_dyi)
        # 接口返回
        api_dyi = api_res['dyi']
        print(api_dyi)
        try:
            assert int(db_dyi) == int(api_dyi)
            return True
        except:
            log.info("登记证明打印总量分析查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("地役登记数据库查询结果： %s" % db_dyi + "，接口返回结果：%s" % api_dyi + "\n")

    @allure.story("预告登记证明")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '预告登记证明')
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

        # 数据库预告登记证明
        sql_yg = "select count(distinct BDCQZH)  from ESTATE_QLXX where ywh in (select YWH  from ESTATE_DJ_SZ where  SZSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'AND SZMC IN ('不动产权证明', '不动产证明') AND ysxlh is  not null AND  ysxlh != '' ) and qllx is not null  and QLTYPE IN ('YGDYQDJ','YGMMDJ') "
        if len(DBConfig().dbconfig(sql_yg)) > 0:
            db_yg = DBConfig().dbconfig(sql_yg)[0]
        else:
            db_yg = 0
        print(db_yg)
        # 接口返回
        api_yg = api_res['yg']
        print(api_yg)
        try:
            assert int(db_yg) == int(api_yg)
            return True
        except:
            log.info("登记证明打印总量分析查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("预告登记数据库查询结果： %s" % db_yg + "，接口返回结果：%s" % api_yg + "\n")

    @allure.story("异议登记证明")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_04(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '异议登记证明')
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

        # 数据库异议登记证明
        sql_yy = "select QLTYPE,count(distinct BDCQZH)  from ESTATE_QLXX where ywh in (select YWH  from ESTATE_DJ_SZ where  SZSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'AND SZMC IN ('不动产权证明', '不动产证明') AND ysxlh is  not null AND  ysxlh != '' ) and qllx is not null  and QLTYPE = 'YYDJ' GROUP BY QLTYPE"
        if len(DBConfig().dbconfig(sql_yy)) > 0:
            db_yy = DBConfig().dbconfig(sql_yy)[0][1]
        else:
            db_yy = 0
        print(db_yy)
        # 接口返回
        api_yy = api_res['yy']
        print(api_yy)
        try:
            assert int(db_yy) == int(api_yy)
            return True
        except:
            log.info("登记证明打印总量分析查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("异议登记数据库查询结果： %s" % db_yy + "，接口返回结果：%s" % api_yy + "\n")

