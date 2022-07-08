# 导入mysql包
import pymssql
from utils.LogUtil import *

# mysql封装
class Mssql:
    # 初始化数据，连接数据库
    def __init__(self, host, user, password, database, charset="utf8", port=1433):
        self.log = Log.logger
        self.conn = pymssql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
            )
        # 获取执行sql的光标对象
        self.cursor = self.conn.cursor()

    # 创建查询、执行方法
    def fetchone(self,sql):
        """
        单个查询
        :return:
        """
        self.cursor.execute(sql)
        # 返回结果
        return self.cursor.fetchone()

    def fetchall(self,sql):
        """
        多个查询
        :return:
        """
        self.cursor.execute(sql)
        # 返回结果
        return self.cursor.fetchall()
    # 执行
    def exec(self,sql):
        """
        执行
        :return:
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            self.log.error("Mysql 执行失败")
            self.log.error(ex)
            return False
        return True

    # 关闭对象
    def __del__(self):
        # 关闭光标对象
        if self.cursor is not None:
            self.cursor.close()
        # 关闭连接对象
        if self.conn is not None:
            self.conn.close()

if __name__ == "__main__":
    mssql = Mssql("114.116.242.198",
                  "sa",
                  "TYht@1234",
                  "estate_test_zws"
                  )
    sql = "SELECT * FROM ESTATE_DCB_H where BDCDYH = '640502221014GB00089F00020490'"
    res = mssql.fetchall(sql)
    mssql.exec(sql)
    print(res)
    # 创建db_cong.yaml,db1,db2
    # 编写数据库基本信息
    # 重构Conf.py
    # 执行


""""
# 连接database
conn = pymysql.connect(
    host = "121.36.92.211",
    port = 8080,
    user = "test",
    password = "123456",
    database = "estate_nxrx",
    charset = "utf8"
)
# 获取执行sql的光标对象
cursor = conn.cursor()
# 执行sql
sql = "select username,password from tb_users"
cursor.execute(sql)
# 执行sql的结果
res = cursor.fetchone()
print(res)
# 关闭对象
cursor.close()
conn.close()
"""