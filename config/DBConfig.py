import pymssql
from utils.DBUtils import *
from utils.LogUtil import Log


class DBConfig:

    def dbconfig(self, sql):
        # 211环境
        conn = Mssql("114.116.242.198",
              "sa",
              "TYht@1234",
              "estate_test_zws")

        # 55环境
        # conn = Mssql("172.19.214.31",
        #              "nxbdcw",
        #              "ZbFkbCC32&b46",
        #              "estate_ycsq_815")
        db_res = conn.fetchall(sql)
        return db_res
