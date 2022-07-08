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


@allure.feature("抵押登记情况-期内新增")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getMortgageInfo.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("抵押登记数量")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '抵押登记数量')
        # 获取yaml文件的内容
        url = url_path + data_list["url"]
        params = data_list["request"]["params"]
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

        # 数据库抵押登记数量
        sql = "SELECT count(1)  FROM (SELECT ROW_NUMBER() OVER(PARTITION BY YWH ORDER BY ZQSE DESC) AS ROW_INDEX,* FROM (SELECT DISTINCT  Q.YWH, (CASE WHEN ISNULL(Q.BDBZZQSE, 0) = 0 THEN ISNULL(Q.ZGZQSE, 0) ELSE Q.BDBZZQSE END) AS ZQSE, S.PROCESS_NAME, CONVERT(VARCHAR(100), Q.DJSJ, 23) SJ FROM ESTATE_QL_DYAQ Q LEFT JOIN ESTATE_PROCESS S ON Q.YWH = S.YWH LEFT JOIN ESTATE_QLXX QLXX ON Q.YWH = QLXX.YWH AND Q.BDCDYH = QLXX.BDCDYH WHERE Q.DJSJ BETWEEN '%s" % startDay \
              + "' and '%s" % endDay + " 23:59:59.000'AND QLXX.DJDL = '100' AND  Q.QSZT in ('1','2'))T) TEMP WHERE ROW_INDEX = 1"

        if len(DBConfig().dbconfig(sql)) > 0:
            db_num = DBConfig().dbconfig(sql)[0][0]
        else:
            db_num = 0
        print(db_num)
        # 接口返回
        api_num = api_res['num']
        print(api_num)

        try:
            assert int(db_num) == int(api_num)
            return True
        except:
            log.error("抵押登记情况-期内新增查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("抵押登记数量数据库查询结果： %s" % db_num + "，接口返回结果：%s" % api_num + "\n")
            raise

    @allure.story("抵押金额")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '抵押金额')
        # 获取yaml文件的内容
        url = url_path + data_list["url"]
        params = data_list["request"]["params"]
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

        # 数据库抵押金额
        sql_zqse = "SELECT  sum(ZQSE) FROM (SELECT ROW_NUMBER() OVER(PARTITION BY YWH ORDER BY ZQSE DESC) AS ROW_INDEX,* FROM (SELECT DISTINCT  Q.YWH, (CASE WHEN ISNULL(Q.BDBZZQSE, 0) = 0 THEN ISNULL(Q.ZGZQSE, 0) ELSE Q.BDBZZQSE END) AS ZQSE, S.PROCESS_NAME, CONVERT(VARCHAR(100), Q.DJSJ, 23) SJ FROM ESTATE_QL_DYAQ Q LEFT JOIN ESTATE_PROCESS S ON Q.YWH = S.YWH LEFT JOIN ESTATE_QLXX QLXX ON Q.YWH = QLXX.YWH AND Q.BDCDYH = QLXX.BDCDYH WHERE Q.DJSJ BETWEEN '%s" % startDay \
                   + "' and '%s" % endDay + " 23:59:59.000'AND QLXX.DJDL = '100' AND  Q.QSZT in ('1','2'))T) TEMP WHERE ROW_INDEX = 1  "

        if len(DBConfig().dbconfig(sql_zqse)) > 0:
            db_zqse = DBConfig().dbconfig(sql_zqse)[0][0]
            if db_zqse is None:
                db_zqse = 0
        else:
            db_zqse = 0
        print(db_zqse)
        # 接口返回
        api_zqse = api_res['zqse']
        print(api_zqse)

        try:
            assert int(db_zqse) == int(api_zqse)
            return True
        except:
            log.error("抵押登记情况-期内新增查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("抵押登记金额数据库查询结果： %s" % db_zqse + "，接口返回结果：%s" % api_zqse + "\n")
            raise

    @allure.story("抵押登记面积")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '抵押登记面积')
        # 获取yaml文件的内容
        url = url_path + data_list["url"]
        params = data_list["request"]["params"]
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

        # 数据库抵押金额
        sql_zqse = "SELECT SUM(MJ) AS JZMJ FROM (" \
                   "SELECT YWH, (CASE WHEN isnull(SCJZMJ, 0) = 0 THEN isnull(YCJZMJ, 0) ELSE SCJZMJ END) MJ FROM ESTATE_FC_H WHERE YWH IN ( SELECT ywh FROM (SELECT ROW_NUMBER() OVER(PARTITION BY YWH ORDER BY ZQSE DESC) AS ROW_INDEX,* FROM (SELECT DISTINCT  Q.YWH, (CASE WHEN ISNULL(Q.BDBZZQSE, 0) = 0 THEN ISNULL(Q.ZGZQSE, 0) ELSE Q.BDBZZQSE END) AS ZQSE, S.PROCESS_NAME, CONVERT(VARCHAR(100), Q.DJSJ, 23) SJ FROM ESTATE_QL_DYAQ Q LEFT JOIN ESTATE_PROCESS S ON Q.YWH = S.YWH LEFT JOIN ESTATE_QLXX QLXX ON Q.YWH = QLXX.YWH AND Q.BDCDYH = QLXX.BDCDYH WHERE Q.DJSJ  " \
                   "BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' " \
                   "AND QLXX.DJDL = '100' AND  Q.QSZT in ('1','2') and S.PROCESS_NAME in ('抵押权首次登记(房屋)','国有建设用地上房屋所有权转本位登记','在建工程抵押权首次登记','在建工程抵押权首次登记(大批量)','在建工程抵押权首次登记(大批量起草)','在建建筑物抵押权首次登记') " \
                   " )T) TEMP WHERE ROW_INDEX = 1   ) " \
                   "union all " \
                   "SELECT DISTINCT YWH,  TDSYQMJ FROM ESTATE_TD_ZDJBXX WHERE YWH IN ( SELECT ywh FROM (SELECT ROW_NUMBER() OVER(PARTITION BY YWH ORDER BY ZQSE DESC) AS ROW_INDEX,* FROM (SELECT DISTINCT  Q.YWH, (CASE WHEN ISNULL(Q.BDBZZQSE, 0) = 0 THEN ISNULL(Q.ZGZQSE, 0) ELSE Q.BDBZZQSE END) AS ZQSE, S.PROCESS_NAME, CONVERT(VARCHAR(100), Q.DJSJ, 23) SJ FROM ESTATE_QL_DYAQ Q LEFT JOIN ESTATE_PROCESS S ON Q.YWH = S.YWH LEFT JOIN ESTATE_QLXX QLXX ON Q.YWH = QLXX.YWH AND Q.BDCDYH = QLXX.BDCDYH WHERE Q.DJSJ " \
                   "BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' AND QLXX.DJDL = '100' AND " \
                   "Q.QSZT in ('1','2') and S.PROCESS_NAME in ('抵押权首次登记(农用地)','抵押权首次登记(土地)','在建工程抵押权首次登记','在建工程抵押权首次登记(大批量)','在建工程抵押权首次登记(大批量起草)','在建建筑物抵押权首次登记') " \
                   ")T) TEMP WHERE ROW_INDEX = 1 ) " \
                   "union all " \
                   "SELECT YWH, ISNULL(FTTDMJ, 0) + (CASE WHEN ISNULL(DYTDMJ, 0) = 0 THEN ISNULL(GYTDMJ, 0) ELSE DYTDMJ END) AS MJ  FROM ESTATE_FC_H  WHERE YWH IN ( SELECT ywh FROM (SELECT ROW_NUMBER() OVER(PARTITION BY YWH ORDER BY ZQSE DESC) AS ROW_INDEX,* FROM (SELECT DISTINCT  Q.YWH, (CASE WHEN ISNULL(Q.BDBZZQSE, 0) = 0 THEN ISNULL(Q.ZGZQSE, 0) ELSE Q.BDBZZQSE END) AS ZQSE, S.PROCESS_NAME, CONVERT(VARCHAR(100), Q.DJSJ, 23) SJ FROM ESTATE_QL_DYAQ Q LEFT JOIN ESTATE_PROCESS S ON Q.YWH = S.YWH LEFT JOIN ESTATE_QLXX QLXX ON Q.YWH = QLXX.YWH AND Q.BDCDYH = QLXX.BDCDYH WHERE Q.DJSJ " \
                   " BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' AND QLXX.DJDL = '100' AND " \
                   "Q.QSZT in ('1','2') and S.PROCESS_NAME in ('土地及地上建筑物抵押权首次登记') " \
                   ")T) TEMP WHERE ROW_INDEX = 1   )" \
                   ") TEMP"

        if len(DBConfig().dbconfig(sql_zqse)) > 0:
            db_zqse = DBConfig().dbconfig(sql_zqse)[0][0]
            if db_zqse is None:
                db_zqse = 0
        else:
            db_zqse = 0
        print(db_zqse)
        # 接口返回
        api_zqse = api_res['area'] * 10000
        print(api_zqse)

        try:
            assert int(db_zqse) == int(api_zqse)
            return True
        except:
            log.error("抵押登记情况-期内新增查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("抵押登记面积数据库查询结果： %s" % db_zqse + "平方米，接口返回结果：%s" % api_zqse + "平方米\n")
            raise