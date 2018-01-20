# -*- coding:utf-8 -*-
import os
#import pymysql
import cx_Oracle
import requests
import json
import time

#pymysql.install_as_MySQLdb()

os.environ["NLS_LANG"] = ".zhs16gbk"

#根据推荐人编号获取营业部编号
def get_branchno(recommendno):
    jsonContent = requests.post('https://www.glsc.com.cn/khv4/servlet/json?funcNo=501571&staff_id=%s'%(recommendno)).text
    target = json.loads(jsonContent)
    error_no = target['error_no']
    if error_no == '0' :
        if target['results'] != []:
            branch_no = ((target['results'])[0])['branch_no']
            return branch_no
        else:
            print('没有找到对应的营业部！推荐人编号为：%s'%recommendno)
            return ''
    else:
        print('查询营业部出错！')



while True:   
    #DB = pymysql.connect('localhost', 'root', '111111', 'testdb1')#连接数据库MYSQL
    DB = cx_Oracle.connect('FXCSTK_ZT/FXCSTK_ZT@172.16.199.122:1521/fxcdb3')#连接ORACLE
    cursor = DB.cursor()

    #查询有问题的数据
    sql = 'SELECT a.user_id, a.recommendno FROM t_stkkh_cust_oareq a, t_stkkh_origin_record b ' \
        'WHERE a.USER_ID = b.USER_ID AND a.RECOMMENDNO IS NOT NULL AND b.SIGN_CHANNEL IS NOT NULL'
    print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print('查询数据失败！')
        DB.rollback()

    #修改营业部号并删除网金标记
    if results != ():
        for i in results:
            print(i[0], i[1])
            branch_no = get_branchno(i[0])
            if branch_no != '':
                sql2 = 'update t_stkkh_cust_oareq set branch_no = %s where user_id = %s'%(branch_no, i[0])
                try:
                    cursor.execute(sql2)
                    DB.commit()
                    sql3 = 'delete from t_stkkh_origin_record where user_id = %s'%(i[0])
                    cursor.execute(sql3)
                    DB.commit()
                    print('数据修改成功！！！客户编号为：%s'%(i[0]))
                except:
                    print('修改营业部号失败，客户编号为%s,推荐人编号为%s'%(i[0],i[1]))
                    DB.rollback()
    else:
        print('没有需要处理的数据！！！')

    cursor.close()
    DB.close()
    del results

    for i in range(1, 6):
        print('已等待%s秒。。。'%i)
        i+=1
        time.sleep(1)