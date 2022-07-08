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


@allure.feature("登记证书打印总量分析")
class Test_1_1:
    # 获取测试用例内容list
    test_file1 = os.path.join(case_path, "getCertificateTotalByQllx.yaml")
    # 使用工具类来读取多个文档内容
    data_list1 = YamlReader(test_file1).data_all()

    @allure.story("登记证书打印总量分析")
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
        # 接口返回
        api_jttd = api_res['jttd']
        api_gyjsyd = api_res['gyjsyd']
        api_jtjsyd = api_res['jtjsyd']
        api_zjd = api_res['zjd']
        api_hy = api_res['hy']
        api_gyjsydfw = api_res['gyjsydfw']
        api_jtjsydfw = api_res['jtjsydfw']
        api_zjdfw = api_res['zjdfw']
        api_hygjw = api_res['hygjw']
        api_nyd = api_res['nyd']
        api_ldcbsllm = api_res['ldcbsllm']
        api_tdcb = api_res['tdcb']

        startDay = params['startDay']
        endDay = params['endDay']
        # 数据库首次登记
        sql = "select dbo.GET_DICT_LABLE(QLLX,'权利类型'),count(distinct BDCQZH)  from ESTATE_QLXX where ywh in (select YWH  from ESTATE_DJ_SZ where  SZSJ BETWEEN '%s"%startDay+"' and '%s"%endDay+" 23:59:59.000'AND SZMC IN ('不动产权证书', '不动产权', '不动产权证') AND ysxlh is  not null AND  ysxlh != '' ) and qllx is not null GROUP BY QLLX"
        db_res = DBConfig().dbconfig(sql)
        print(db_res)
        global db_jttd,db_gyjsyd,db_jtjsyd,db_zjd,db_hy,db_gyjsydfw,db_jtjsydfw,db_zjdfw,db_hygjw,db_nyd,db_ldcbsllm,db_tdcb
        db_jttd = 0
        db_gyjsyd = 0
        db_jtjsyd = 0
        db_zjd = 0
        db_hy = 0
        db_gyjsydfw = 0
        db_jtjsydfw = 0
        db_zjdfw = 0
        db_hygjw = 0
        db_nyd = 0
        db_ldcbsllm = 0
        db_tdcb = 0
        if len(db_res) > 0:
            for item in db_res:
                print(item)
                if item[0] == '集体土地所有权':
                    print(item[1])
                    db_jttd = item[1]
                elif item[0] == '国有建设用地使用权':
                    print(item[1])
                    db_gyjsyd = item[1]
                elif item[0] == '集体建设用地使用权':
                    print(item[1])
                    db_jtjsyd = item[1]
                elif item[0] == '宅基地使用权':
                    print(item[1])
                    db_zjd = item[1]
                elif item[0] == '海域（含无居民海岛）使用权':
                    print(item[1])
                    db_hy = item[1]
                elif item[0] == '国有建设用地使用权/房屋所有权':
                    print(item[1])
                    db_gyjsydfw = item[1]
                elif item[0] == '集体建设用地使用权/房屋（构筑物）所有权':
                    print(item[1])
                    db_jtjsydfw = item[1]
                elif item[0] == '宅基地使用权/房屋（构筑物）所有权':
                    print(item[1])
                    db_zjdfw = item[1]
                elif item[0] == '海域（含无居民海岛）使用权/房屋（构筑物）所有权':
                    print(item[1])
                    db_hygjw = item[1]
                elif item[0] == '农用地使用权（非林地）':
                    print(item[1])
                    db_nyd = item[1]
                elif item[0] == '林地承包经营权、使用权/森林、林木所有权':
                    print(item[1])
                    db_ldcbsllm = item[1]
                elif item[0] == '土地承包经营权':
                    print(item[1])
                    db_tdcb = item[1]

        try:
            assert int(api_jttd) == int(db_jttd) and \
                   int(api_gyjsyd) == int(db_gyjsyd) and \
                   int(api_jtjsyd) == int(db_jtjsyd) and \
                   int(api_zjd) == int(db_zjd) and \
                   int(api_hy) == int(db_hy) and \
                   int(api_gyjsydfw) == int(db_gyjsydfw) and \
                   int(api_jtjsydfw) == int(db_jtjsydfw) and \
                   int(api_zjdfw) == int(db_zjdfw) and \
                   int(api_hygjw) == int(db_hygjw) and \
                   int(api_nyd) == int(db_nyd) and \
                   int(api_ldcbsllm) == int(db_ldcbsllm) and \
                   int(api_tdcb) == int(db_tdcb)
            return True
        except:
            log.error("登记证书打印总量分析查询，条件开始时间： %s" % startDay + "，结束时间：%s" % endDay + "\n")
            if int(api_jttd) != int(db_jttd):
                log.error("集体土地所有权数据库查询结果： %s" % db_jttd + "，接口返回结果：%s" % api_jttd + "\n")
            if int(api_gyjsyd) != int(db_gyjsyd):
                log.error("国有建设用地使用权数据库查询结果： %s" % db_gyjsyd + "，接口返回结果：%s" % api_gyjsyd + "\n")
            if int(api_jtjsyd) != int(db_jtjsyd):
                log.error("集体建设用地使用权数据库查询结果： %s" % db_jtjsyd + "，接口返回结果：%s" % api_jtjsyd + "\n")
            if int(api_zjd) != int(db_zjd):
                log.error("宅基地使用权数据库查询结果： %s" % db_zjd + "，接口返回结果：%s" % api_zjd + "\n")
            if int(api_hy) != int(db_hy):
                log.error("海域（含无居民海岛）使用权数据库查询结果： %s" % db_hy + "，接口返回结果：%s" % api_hy + "\n")
            if int(api_gyjsydfw) != int(db_gyjsydfw):
                log.error("国有建设用地使用权/房屋所有权数据库查询结果： %s" % db_gyjsydfw + "，接口返回结果：%s" % api_gyjsydfw + "\n")
            if int(api_jtjsydfw) != int(db_jtjsydfw):
                log.error("集体建设用地使用权/房屋（构筑物）所有权数据库查询结果： %s" % db_jtjsydfw + "，接口返回结果：%s" % api_jtjsydfw + "\n")
            if int(api_zjdfw) != int(db_zjdfw):
                log.error("宅基地使用权/房屋（构筑物）所有权数据库查询结果： %s" % db_zjdfw + "，接口返回结果：%s" % api_zjdfw + "\n")
            if int(api_hygjw) != int(db_hygjw):
                log.error("海域（含无居民海岛）使用权/房屋（构筑物）所有权数据库查询结果： %s" % db_hygjw + "，接口返回结果：%s" % api_hygjw + "\n")
            if int(api_nyd) == int(db_nyd):
                log.error("农用地使用权（非林地）数据库查询结果： %s" % db_nyd + "，接口返回结果：%s" % api_nyd + "\n")
            if int(api_ldcbsllm) != int(db_ldcbsllm):
                log.error("林地承包经营权、使用权/森林、林木所有权数据库查询结果： %s" % db_ldcbsllm + "，接口返回结果：%s" % api_ldcbsllm + "\n")
            if int(api_tdcb) != int(db_tdcb):
                log.error("土地承包经营权数据库查询结果： %s" % db_tdcb + "，接口返回结果：%s" % api_tdcb + "\n")
            raise

