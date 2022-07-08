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

pytestmark = pytest.mark.zx
request = Request()
# 统一接口路径
url_path = ConfigYaml().get_conf_url()
# 用例数据文件路径
case_path = Path.get_testcase_path() + "test_01"

# 获取测试用例内容list
# 获取testlogin.yaml文件路径
test_file = os.path.join(case_path, "test1.yaml")
# 使用工具类来读取多个文档内容
data_list = YamlReader(test_file).data_all()


@allure.story("登录")
@pytest.mark.parametrize("login", data_list)
# 参数化执行测试用例
def test_1_interface_1(login):
    # 报告用例标题
    allure.dynamic.title(login["case_name"])
    # 初始化url,data
    url = ConfigYaml().get_conf_url()+login["url"]
    params = login["request"]["params"]
    params["username"] = globalVar.username
    params["password"] = globalVar.password
    service = params["service"]
    appKey = params["appKey"]
    expectcode = login["expect"]["code"]
    # post请求
    res = request.get(url+"?username=%s"%globalVar.username+"&password=%s"%globalVar.password+"&service=%s"%(url_path+service)+"&appKey=%s"%appKey,json=params)
    # res = request.get(url+"?username=%s"%globalVar.username+"&password=%s"%globalVar.password+"&service=%s"%(url_path+service)+"&appKey=%s"%appKey+"&captcha=y4wp5d",json=params)

    tok = res["body"]["data"]["gmsso_cli_ec_key"]
    #设置全局变量
    globalVar.set_value('tok',tok)
    appKey = res["body"]["data"]["appKey"]
    # 设置全局变量
    globalVar.set_value('appKey',appKey)
    code = res["code"]
    body = res["body"]
    gmsso_cli_ec_key = res['body']['data']['gmsso_cli_ec_key']
    gmsso_ser_ec_key = res['body']['data']['gmsso_ser_ec_key']
    globalVar.Cookie = 'Cookie=JSESSIONID=CFEC720F613AC9D73E20E1C8B82B26D8; BDC_REGISTER=%s' % gmsso_cli_ec_key + '; clientServerToken=%s' % gmsso_ser_ec_key

    AssertUtil().assert_code(code, expectcode)
    AssertUtil().assert_in_body(body,'"success": true')