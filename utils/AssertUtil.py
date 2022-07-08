from utils.LogUtil import *
import json
# 断言装类
class AssertUtil:
    # 初始化数据，日志
    def __init__(self):
        self.log = Log.logger

    # code相等
    def assert_code(self,code,excepted_code):
        """
        验证返回状态吗
        :param code:
        :param excepted_code:
        :return:
        """
        try:
            assert int(code) == int(excepted_code)
            return True
        except:
            self.log.error("code error,code is %s,excepted_code is %s"%(code,excepted_code))
            raise

    # body相等
    def assert_body(self,body,excepted_body):
        """
        验证返回结果内容相等
        :param body:
        :param excepted_body:
        :return:
        """
        try:
            assert body == excepted_body
            return True
        except:
            self.log.error("body error,body is %s,excepted_body is %s"%(body,excepted_body))
            raise

    # body包含
    def assert_in_body(self,body,excepted_body):
        """
        验证返回结果是否包含期望结果
        :param body:
        :param excepted_body:
        :return:
        """
        try:
            body = json.dumps(body)
            assert excepted_body in body
            return True
        except:
            self.log.error("不包含或者body是错误，body is %s,excepted_body is %s"%(body,excepted_body))
            raise