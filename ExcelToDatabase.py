# -*- coding:utf-8 -*-
import pymysql
import xlrd
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()

FILDE_NAME = ''  # 拼接后的字段字符串
CELL_LST = []  # 表头字段列表

f_data = xlrd.open_workbook('test.xlsx') #读取工作簿
table = f_data.sheets()[0] #读取第一张工作表

n_rows = table.nrows  # 获取行数
n_cols = table.ncols  # 获取列数

engine = create_engine(
    "mysql+mysqldb://root:111111@localhost:3306/testdb1?charset=utf8", max_overflow=5)

for j in range(n_rows):
    if j == 0:
        #第一行为作为表头字段
        for i in range(n_cols):
            CELL_LST.append(str(table.cell(j, i).value))
        FILDE_NAME = ','.join(CELL_LST)  # 格式化字段字符串，用逗号分隔
    else:
        #第二行开始循环读取和插入值
        val_lst = []  # 值列表
        for i in range(n_cols):
            if isinstance(table.cell(j, i).value, float):
                print('进入数据转换')
                cell_var = '\'%s\''%(int(table.cell(j, i).value))
            else:
                cell_var = '\'%s\''%(str(table.cell(j, i).value))
            val_lst.append(cell_var)
        vals = ','.join(val_lst)  # 格式化值字符串，用逗号分隔
        print(vals)
        sql = 'INSERT INTO testdb1.pythontest(%s) VALUES (%s)'%(FILDE_NAME, vals)
        print(sql)
        try:
            engine.execute(sql)
        except:
            print('插入数据失败！')
        val_lst.clear()  # 清空值列表
