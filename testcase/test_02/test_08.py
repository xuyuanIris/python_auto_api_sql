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

# 获取测试用例内容list
test_file1 = os.path.join(case_path, "getPersonalBusinessTotal.yaml")
# 使用工具类来读取多个文档内容
data_list1 = YamlReader(test_file1).data_all()

@allure.feature("工作人员办件量-办理节点")
class Test_1_1:

    @allure.story("登簿节点")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '登簿节点')
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

        api_res = r['body']['data']['personalTaskKeyTotal']['db']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 受理节点办件总量
        sql = "SELECT task_key, count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and task_key='登簿' GROUP BY  task_key"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res['total']
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("登簿节点办件总量数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("受理节点")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '受理节点')
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

        api_res = r['body']['data']['personalTaskKeyTotal']['sl']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 受理节点办件总量
        sql = "SELECT task_key, count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and task_key='受理' GROUP BY  task_key"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res['total']
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("受理节点办件总量数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("初审节点")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '初审节点')
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

        api_res = r['body']['data']['personalTaskKeyTotal']['cs']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 受理节点办件总量
        sql = "SELECT task_key, count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and task_key='初审' GROUP BY  task_key"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res['total']
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("初审节点办件总量数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("复审节点")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_04(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '复审节点')
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

        api_res = r['body']['data']['personalTaskKeyTotal']['fs']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 受理节点办件总量
        sql = "SELECT task_key, count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and task_key='复审' GROUP BY  task_key"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res['total']
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("复审节点办件总量数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("核定节点")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_05(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '核定节点')
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

        api_res = r['body']['data']['personalTaskKeyTotal']['hd']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 受理节点办件总量
        sql = "SELECT task_key, count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and task_key='核定' GROUP BY  task_key"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res['total']
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("核定节点办件总量数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("缮证节点")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_06(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '缮证节点')
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

        api_res = r['body']['data']['personalTaskKeyTotal']['sz']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 缮证节点办件总量
        sql = "SELECT task_key, count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and task_key='缮证' GROUP BY  task_key"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res['total']
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("缮证节点办件总量数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("发证节点")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_06(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '发证节点')
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

        api_res = r['body']['data']['personalTaskKeyTotal']['fz']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 发证节点办件总量
        sql = "SELECT task_key, count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and task_key='发证' GROUP BY  task_key"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res['total']
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("发证节点办件总量数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise


@allure.feature("工作人员办件量-登记类型")
class Test_1_2:

    @allure.story("登记类型-首次登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '首次登记')
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

        api_res = r['body']['data']['bussinessTotal']['sc']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='100' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("首次登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-转移登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_02(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '转移登记')
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

        api_res = r['body']['data']['bussinessTotal']['zy']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='200' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("转移登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-变更登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_03(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '变更登记')
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

        api_res = r['body']['data']['bussinessTotal']['bg']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='300' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("变更登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-注销登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_04(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '注销登记')
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

        api_res = r['body']['data']['bussinessTotal']['zx']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='400' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("注销登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-更正登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_05(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '更正登记')
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

        api_res = r['body']['data']['bussinessTotal']['gz']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='500' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("更正登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-异议登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_06(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '异议登记')
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

        api_res = r['body']['data']['bussinessTotal']['yy']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='600' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("异议登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-预告登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_07(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '预告登记')
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

        api_res = r['body']['data']['bussinessTotal']['yg']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='700' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("预告登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-查封登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_08(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '查封登记')
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

        api_res = r['body']['data']['bussinessTotal']['cf']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='800' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("查封登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise

    @allure.story("登记类型-其它登记")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_09(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"] + '其它登记')
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

        api_res = r['body']['data']['bussinessTotal']['qt']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 办件总量
        sql = "SELECT dbo.GET_DICT_LABLE(DJDL, '登记大类'),  count(DISTINCT ywh)  FROM   (SELECT FLO.*  FROM ( " \
              "SELECT  ROW_NUMBER ( ) OVER ( PARTITION BY INFO.BIZ_KEY ORDER BY INFO.START_TIME DESC) RN, INFO.ID,INFO.BIZ_KEY, INFO.PROCESS_NAME, INFO.TASK_KEY, INFO.TRANSACTOR_NAME, CONVERT(VARCHAR(100), INFO.HANDLE_TIME, 23) SJ,STATUS,HANDLE_TIME " \
              "FROM T_BIZ_FLOW_INFO_HISTORY INFO where INFO.HANDLE_TIME BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000' ) FLO WHERE FLO.RN =1 ) temp left join  ESTATE_QLXX qlxx  on  qlxx.ywh2 = temp.biz_key where ywh like '%01' and DJDL='900' GROUP BY  DJDL"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        if len(db_res) > 0:
            db_total = db_res[0][1]
        else:
            db_total = 0

        # 接口返回
        if api_res is not None:
            api_total = api_res
        else:
            api_total = 0

        try:
            assert int(api_total) == int(db_total)
            return True
        except:
            log.error("工作人员办件量-登记类型查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            log.info("其它登记数据库查询结果： %s" % db_total + "，接口返回结果：%s" % api_total + "\n")
            raise
