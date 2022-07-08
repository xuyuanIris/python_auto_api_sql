""""
数据工厂，解析数据
excel yaml
"""

import os
import re
import tempfile
from xml.etree.ElementTree import ElementTree, Element

class XMLReader:
    """xml文件操作"""
    def __init__(self, path):
        self.path = path
        self.tree = ElementTree()
        self.tree.parse(self.path)

    @staticmethod
    def if_match(node, kv_map):
        """判断某个节点是否包含所有传入参数属性
          node: 节点
          kv_map: 属性及属性值组成的map
        """
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

    def write_xml(self, out_path=None):
        """将xml文件写出
          out_path: 写出路径，不填写则修改自身
        """
        out_path = out_path if out_path else self.path
        self.tree.write(out_path, encoding="utf-8", xml_declaration=True)

    def find_nodes(self, path):
        """查找某个路径匹配的所有节点
          tree: xml树
          path: 节点路径"""
        return self.tree.findall(path)

    @staticmethod
    def get_node_attribute_val(node, attribute):
        """获取节点的指定属性值
          node: 节点
          attribute: 属性
        """
        return node.attrib.get(attribute)

    @staticmethod
    def change_node_text(nodelist, text, is_add=False, is_delete=False):
        """改变/增加/删除一个节点的文本
          nodelist:节点列表
          text : 更新后的文本"""
        for node in nodelist:
            if is_add:
                node.text += text
            elif is_delete:
                node.text = ""
            else:
                node.text = text

    @staticmethod
    def create_node(tag, property_map=None, content=None):
        """新造一个节点
          tag:节点标签
          property_map:属性及属性值map
          content: 节点闭合标签里的文本内容
          return 新节点"""
        element = Element(tag, property_map)
        element.text = content
        return element

    @staticmethod
    def add_child_node(node, element):
        """给一个节点添加子节点
          nodelist: 节点列表
          element: 子节点"""
        node.append(element)


class Properties:
    """properties文件格式处理"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        """判断key是否存在
        :param key:要校验的key
        :return Ture/False
        """
        return key in self.properties

    def get(self, key, default_value=''):
        """获取指定key的值，不存在则返回自定义的字符
        :param key:要获取的key
        :param default_value:自定义返回值
        """
        if key in self.properties:
            return self.properties[key]
        return default_value

    def update(self, key, value):
        """更新所有指定key的值，不存在则添加
        :param key:指定key
        :param value:指定值
        """
        self.properties[key] = value
        self.replace_property(key + '=.*', key + '=' + value, True)
        print(f"{key}更新成功！！！")

    def update_add(self, key, value):
        """更新所有指定key的值，在原来的值后面追加值，以逗号分隔，不存在则添加key之后追加
        :param key:指定key
        :param value:追加的值
        """
        new_value = self.get(key) + "," + value
        self.replace_property(
            key + '=.*',
            key + '=' + new_value,
            True)
        print(f"{key}更新成功！！！")

    def replace_property(self, from_regex, to_str, append_on_not_exists=True):
        tmpfile = tempfile.TemporaryFile()

        if os.path.exists(self.file_name):
            r_open = open(self.file_name, 'r')
            pattern = re.compile(r'' + from_regex)
            found = None
            for line in r_open:
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    line = re.sub(from_regex, to_str, line)
                tmpfile.write(line.encode())
            if not found and append_on_not_exists:
                tmpfile.write(('\n' + to_str).encode())
            r_open.close()
            tmpfile.seek(0)

            content = tmpfile.read()

            if os.path.exists(self.file_name):
                os.remove(self.file_name)

            w_open = open(self.file_name, 'wb')
            w_open.write(content)
            w_open.close()

            tmpfile.close()
        else:
            print(f"file {self.file_name} not found")


if __name__ == '__main__':
    excel_path = r'E:\PycharmProjects\estate_hn\testcase\data\测试数据.xlsx'
    # data = ExcelReader(excel_path, 1).data
    # print(data)
