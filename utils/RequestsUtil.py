import requests
import allure
from utils.LogUtil import *

# 创建get方法请求
def requests_get(url,headers=None):
    # 发送requests  get请求
    r = requests.get(url,headers = headers)
    # 获取结果相应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
    # 将内容存到字典
    res = dict()
    res["code"] = code
    res["body"] = body
    # 字典返回
    return res

# 创建post方法请求
def requests_post(url,json=None,data=None,files=None, headers=None):
    # 发送requests  post请求
    r = requests.post(url, json=json, data=data, files=files, headers=headers)
    # 获取结果相应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
    # 将内容存到字典
    res = dict()
    res["code"] = code
    res["body"] = body
    # 字典返回
    return res

class Request:
    def __init__(self):
        self.log = Log.logger
    def requests_api(self, url, json=None, data=None, params=None, files=None, headers=None, method="get"):
        if method == "get":
            # get请求
            self.log.info("发送get请求")
            r = requests.get(url, json=json, data=data, params=params, files=files, headers=headers)
        elif method == "post":
            # post请求
            self.log.info("发送post请求")
            r = requests.post(url, json=json, data=data, params=params, files=files, headers=headers)

        # 获取结果相应内容
        code = r.status_code
        try:
            body = r.json()
            self.log.info("返回结果:%s" % r.json())
        except Exception as e:
            body = r.content
            self.log.info("返回结果:%s" % r.text)
        # 将内容存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        # 字典返回
        return res

    # 重构get/post
    # get方法
    @allure.step("请求接口")
    def get(self, url, **kwargs):
        """
        发送get请求
        :param url: 接口url
        :param kwargs: 传递参数
        :return: 返回结果
        """
        return self.requests_api(url, method="get", **kwargs)

    # post方法
    @allure.step("请求接口")
    def post(self, url, **kwargs):
        """
        发送post请求
        :param url: 接口url
        :param kwargs: 传递参数
        :return: 返回结果
        """
        return self.requests_api(url, method="post", **kwargs)


