import os
import pandas as pd
import cx_Oracle
import pymysql
from ftplib import FTP
import requests
import json
import psycopg2

HEADERS =  {
    'Authorization':""
}

REFRESH_TOKEN = ''

domain = 'https://dashboard-rmbmss.titan.com/'

def get_data(sql,col_lst):
    #连接数据库
    conn=cx_Oracle.connect('ONL1/Rmb2_2015@200.80.24.87:1521/RMBDB',encoding = 'UTF-8',nencoding = 'UTF-8')
    curs=conn.cursor()
    #获取当日实时成交数据
    curs.execute(sql)
    rows=curs.fetchall()
    #转为dataframe格式
    df=pd.DataFrame(rows)
    if not df.empty:
        df.columns = col_lst
    return df

def get_data_sys(sql,col_lst):
    #连接数据库
    conn=cx_Oracle.connect('SYS/Rmb2_2015@200.80.24.87:1521/RMBDB',encoding = 'UTF-8',nencoding = 'UTF-8',mode = cx_Oracle.SYSDBA)
    curs=conn.cursor()
    #获取当日实时成交数据
    curs.execute(sql)
    rows=curs.fetchall()
    #转为dataframe格式
    df=pd.DataFrame(rows)
    if not df.empty:
        df.columns = col_lst
    return df

def get_mysql_data(sql):
    #连接数据库
    conn=pymysql.connect(host = '127.0.0.1',user = 'root',passwd='root',port = 3306,db='cfets',charset = 'utf8')
    curs=conn.cursor()
    #获取当日实时成交数据
    curs.execute(sql)
    rows=curs.fetchall()
    #转为dataframe格式
    lst = []   
    for i in rows:
        lst.append(list(i))
    return lst

#保留两位小数
def num2(x):
    x = float(x)
    return round(x,2)

#四舍五入
def int2(x):
    x = float(x)
    return int(x+0.5)

#判断境外机构
def get_outland(x):
    if '境外' in x or x == '主权财富基金' or x == '国际金融组织':
        return 1
    else:
        return 0

def upload_ftp(file,path):
    bufsize=1024
    ftp=FTP()
    ftp.connect("200.31.138.9",21)
    ftp.login()
    ftp.encoding='gbk'
    ftp.cwd(path)
    f=open(file,'rb')
    ftp.storbinary("STOR %s"%os.path.basename(file),f,bufsize)
    ftp.set_debuglevel(0)
    f.close()
    ftp.quit()  


def get_loginapi():
    global HEADERS
    global REFRESH_TOKEN
    url = domain + 'loginapi'
    data = {'username':'admin',
            'password':'E5be33Cb967bHf7e'}
    res = requests.get(url,data=data,verify = False)
    js = res.text
    # print('----------------------------------------',js)
    token_js = json.loads(js)
    token = token_js.get('access_token','')
    REFRESH_TOKEN = token_js.get('refresh_token','')
    HEADERS['Authorization'] = 'Bearer ' + token
    # print('accessssssssssssssssssss',HEADERS)
    print('首次登陆，获取token成功')

def get_refreshapi():
    global HEADERS
    global REFRESH_TOKEN

    url = os.path.join(domain , 'refreshapi')
    data = {'rf_token':REFRESH_TOKEN}
    res = requests.get(url,data=data,verify = False)
    js = res.text
    # print('----------------------------------------',js)
    token_js = json.loads(js)
    token = token_js.get('access_token','')
    REFRESH_TOKEN = token_js.get('refresh_token','')
    HEADERS['Authorization'] = 'Bearer ' + token
    # print('refreshhhhhhhhhhhhhhhhhhh',HEADERS)
    print('刷新token成功！！')


def gp_sql(sql):
    url = os.path.join(domain , 'gp_sql')
    data = {'sql':sql}
    res = requests.post(url,data=data,headers=HEADERS,verify = False)
    return res.text

def gp_params(fields,tables,ons,wheres,groups,orders):
    url = os.path.join(domain , 'gp_params')
    data = {'fields':fields,
            'tables':tables,
            'ons':ons,
            'wheres':wheres,
            'groups':groups,
            'orders':orders}

    res = requests.post(url,data=data,headers = HEADERS,verify = False)
    return res.text


def gp_data(js):
    res_js = json.loads(js)
    # print('-----------------------------',res_js)
    data = res_js.get('data')
    df= pd.DataFrame(data)
    col_lst = df.columns

    for key in col_lst:
        try:
            df[key] = df[key].astype(float)
        except:
            continue
    return df


def gp_data2(js):
    res_js = json.loads(js)
    # print('-----------------------------',res_js)
    data = res_js.get('data')
    df= pd.DataFrame(data)
    return df


def pg_select(sql):
    conn = psycopg2.connect(database='sdpdb', user='sdpuser', password='123456', host='200.31.175.88', port='5432')
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows,columns=cols)
    conn.commit()
    conn.close()
    return df
