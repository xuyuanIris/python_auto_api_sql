import requests
import json

from utils.FileReaderUtil import XMLReader
from utils.LogUtil import Log
from config.Conf import RunConfig

logger = Log.logger
def send_wx(xml_path, test_env_config):
    """发送企业微信消息"""
    names = ['timestamp', 'time', 'hostname', 'tests', 'skipped', 'failures', 'errors']
    xml = XMLReader(xml_path)
    testsuite_node = xml.find_nodes('testsuite')[0]
    result = [xml.get_node_attribute_val(testsuite_node, names[i]) for i in range(len(names))]
    xml_data = dict(zip(names, result))

    timestamp = xml_data.get('timestamp')
    data_time = timestamp.split('T')
    end = data_time[0] + ' ' + data_time[1].split('.')[0]
    _time = float(xml_data.get('time'))
    sum_time = f'{int(_time // 3600)}时{int((_time - (_time // 3600) * 3600) // 60)}分{(_time - (_time // 3600) * 3600 - ((_time - (_time // 3600) * 3600) // 60) * 60): .2f}秒'
    tests = xml_data.get('tests')
    skipped = xml_data.get('skipped')
    failures = xml_data.get('failures')
    errors = xml_data.get('errors')
    _pass = str(int(tests) - int(skipped) - int(failures) - int(errors))
    _data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f'#### 本次{test_env_config}环境回归测试已结束，请相关同事注意。\n>开始时间:<font color="comment">{end}</font>\n>历时:<font color="comment">{sum_time}</font>\n>总用例数:<font color="comment">{tests}例</font>\n>>通过:<font color="info">{_pass}例</font>\n跳过:<font color="comment">{skipped}例</font>\n>失败:<font color="warning">{failures}例</font>\n>错误:<font color="warning">{errors}例</font>\n>##### 点击[控制台](http://121.37.107.182:9000/jenkins/job/web%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/job/%E5%AE%81%E5%A4%8F%E7%99%BB%E8%AE%B0%E7%B3%BB%E7%BB%9F%E7%BB%9F%E8%AE%A1%E5%88%86%E6%9E%90211%E7%8E%AF%E5%A2%83/allure/)查看详细测试报告\n>（建议直接登录公司Jenkins可查看项目更多详情）'
        },
        "mentioned_mobile_list": ["13417375072"]
    }
    head = {'Content-Type': 'application/json'}
    data = json.dumps(_data)
    res = requests.post(RunConfig.send_wx_message_url, data, headers=head)
    if res.status_code == 200:
        logger.info('企业微信通知发送成功')
    else:
        logger.info('企业微信通知发送失败')
