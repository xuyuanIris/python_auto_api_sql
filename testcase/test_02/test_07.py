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


@allure.feature("网络查询量")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getWwcdzmCountTotal.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("网络查询量")
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

        code = r["code"]
        AssertUtil().assert_code(code, expectcode)

        api_res = r['body']['data']
        print(api_res)
        startDay = params['startDay']
        endDay = params['endDay']

        # 数据库网络查询量
        sql = "SELECT CDLY, count(*) FROM  ESTATE_EXT_WW_CDZM WHERE CXSJ BETWEEN '%s" % startDay + "' and '%s" % endDay + " 23:59:59.000'and cdly is not null  GROUP BY  CDLY "
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        print(len(db_res))
        global GZH,HLW,JRB,KSTB
        GZH = 0
        HLW = 0
        JRB = 0
        KSTB = 0
        if len(db_res) > 0:
            for item in db_res:
                if item[0] == 'GZH':
                    GZH = item[1]
                elif item[0] == 'HLW':
                    HLW = item[1]
                elif item[0] == 'JRB':
                    JRB = item[1]
                elif item[0] == 'KSTB':
                    KSTB = item[1]
        # 接口返回
        api_hlw = api_res['hlw']
        api_gzh = api_res['gzh']
        api_jrb = api_res['jrb']
        api_kstb = api_res['kstb']

        try:
            assert int(GZH) == int(api_gzh) and int(HLW) == int(api_hlw) and int(JRB) == int(api_jrb) and int(KSTB) == int(api_kstb)
            return True
        except:
            log.error("网络查询量查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(GZH) != int(api_gzh):
                log.info("微信公众号数量数据库查询结果： %s" % GZH + "，接口返回结果：%s" % api_gzh + "\n")
            if int(HLW) != int(api_hlw):
                log.info("互联网+不动产量数据库查询结果： %s" % HLW + "，接口返回结果：%s" % api_hlw + "\n")
            if int(JRB) != int(api_jrb):
                log.info("金融管理量数据库查询结果： %s" % JRB + "，接口返回结果：%s" % api_jrb + "\n")
            if int(KSTB) != int(api_kstb):
                log.info("跨省通办量数据库查询结果： %s" % KSTB + "，接口返回结果：%s" % api_kstb + "\n")
            raise



