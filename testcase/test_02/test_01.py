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


@allure.feature("业务量总量分析")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getBusinessTotal.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("业务量总量分析")
    @pytest.mark.parametrize("data_list", data_list1)
    def test_1_interface_01(self, data_list):
        # 报告标题
        allure.dynamic.title(data_list["case_name"])
        # 获取yaml文件的内容
        url = url_path + data_list["url"]
        params = data_list["request"]["params"]
        params['regionCode'] = globalVar.regionCode
        params['areaCode'] = globalVar.areaCode
        headers = data_list["request"]["headers"]
        headers['Cookie'] = globalVar.cookie
        expectcode = data_list["expect"]["code"]
        r = request.post(url, data=params, headers=headers)
        print(r)
        code = r["code"]
        AssertUtil().assert_code(code, expectcode)

        api_res = r['body']['data']
        startDay = params['startDay']
        endDay = params['endDay']
        # 数据库首次登记
        sql = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '100' and QSZT !='3' AND SLSJ BETWEEN '%s"%startDay+"' and '%s"%endDay+" 23:59:59.000'"
        if len(DBConfig().dbconfig(sql)) > 0:
            db_sc = DBConfig().dbconfig(sql)[0][0]
        else:
            db_sc = 0
        print(db_sc)
        # 接口返回的首次
        api_sc = api_res['sc']

        # 数据库转移登记
        sql_zy = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '200' and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_zy)) > 0:
            db_zy = DBConfig().dbconfig(sql_zy)[0][0]
        else:
            db_zy = 0
        print(db_zy)
        # 接口返回的转移
        api_zy = api_res['zy']

        # 数据库变更登记
        sql_bg = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '300' and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_bg)) > 0:
            db_bg = DBConfig().dbconfig(sql_bg)[0][0]
        else:
            db_bg = 0
        print(db_bg)
        # 接口返回的变更
        api_bg = api_res['bg']

        # 数据库注销登记
        sql_zx = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '400' and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_zx)) > 0:
            db_zx = DBConfig().dbconfig(sql_zx)[0][0]
        else:
            db_zx = 0
        print(db_zx)
        # 接口返回的注销
        api_zx = api_res['zx']

        # 数据库更正登记
        sql_gz = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '500' and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_gz)) > 0:
            db_gz = DBConfig().dbconfig(sql_gz)[0][0]
        else:
            db_gz = 0
        print(db_gz)
        # 接口返回的注销
        api_gz = api_res['gz']

        # 数据库异议登记
        sql_yy = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '600' and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_yy)) > 0:
            db_yy = DBConfig().dbconfig(sql_yy)[0][0]
        else:
            db_yy = 0
        print(db_yy)
        # 接口返回的注销
        api_yy = api_res['yy']

        # 数据库预告登记
        sql_yg = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '700' and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_yg)) > 0:
            db_yg = DBConfig().dbconfig(sql_yg)[0][0]
        else:
            db_yg = 0
        print(db_yg)
        # 接口返回的注销
        api_yg = api_res['yg']

        # 数据库查封登记
        sql_cf = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL = '800' and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_cf)) > 0:
            db_cf = DBConfig().dbconfig(sql_cf)[0][0]
        else:
            db_cf = 0
        print(db_cf)
        # 接口返回的注销
        api_cf = api_res['cf']

        # 数据库其他登记
        sql_qt = "select count(DISTINCT YWH) from ESTATE_QLXX where DJDL in ('900','998') and QSZT !='3' AND SLSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'"
        if len(DBConfig().dbconfig(sql_qt)) > 0:
            db_qt = DBConfig().dbconfig(sql_qt)[0][0]
        else:
            db_qt = 0
        print(db_qt)
        # 接口返回的注销
        api_qt = api_res['qt']

        try:
            assert api_sc == db_sc and \
                   api_zy == db_zy and \
                   api_bg == db_bg and \
                   api_zx == db_zx and \
                   api_gz == db_gz and \
                   api_yy == db_yy and \
                   api_yg == db_yg and \
                   api_cf == db_cf and \
                   api_qt == db_qt
            return True
        except:
            log.error("业务量总量分析查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if api_qt != db_qt:
                log.error("其他登记数据库查询结果： %s" % db_qt + "，接口返回结果：%s" % api_qt + "\n")
            if api_sc != db_sc:
                log.error("首次登记数据库查询结果： %s" % db_sc + "，接口返回结果：%s" % api_sc + "\n")
            if api_zy != db_zy:
                log.error("转移登记数据库查询结果： %s" % db_zy + "，接口返回结果：%s" % api_zy + "\n")
            if api_bg != db_bg:
                log.error("变更登记数据库查询结果： %s" % db_bg + "，接口返回结果：%s" % api_bg + "\n")
            if api_zx != db_zx:
                log.error("注销登记数据库查询结果： %s" % db_zx + "，接口返回结果：%s" % api_zx + "\n")
            if api_gz != db_gz:
                log.error("更正登记数据库查询结果： %s" % db_gz + "，接口返回结果：%s" % api_zx + "\n")
            if api_yy != db_yy:
                log.error("异议登记数据库查询结果： %s" % db_yy + "，接口返回结果：%s" % api_yy + "\n")
            if api_yg != db_yg:
                log.error("预告登记数据库查询结果： %s" % db_yg + "，接口返回结果：%s" % api_yg + "\n")
            if api_cf != db_cf:
                log.error("查封登记数据库查询结果： %s" % db_cf + "，接口返回结果：%s" % api_cf + "\n")
            raise

