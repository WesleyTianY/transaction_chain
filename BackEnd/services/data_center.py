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

def pg_select(sql, params=None):
    conn = psycopg2.connect(database='sdpdb', user='sdpuser', password='123456', host='200.31.175.88', port='5432')
    cur = conn.cursor()
    # cur.execute(sql)
    cur.execute(sql, params)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows,columns=cols)
    conn.commit()
    conn.close()
    return df

def get_transaction_data1(date):
    # 将参数 `date` 动态地插入到 SQL 查询中
    sql = f"""
    select *
    from dpa.cbt_dl_dtl
    where txn_dt = %s and trdng_md_cd = 'NDM'
    limit 30000
    """
    # 使用参数化查询执行 SQL
    df_trade = pg_select(sql, (date,))
    columns_to_export = [
        'dl_cd', 'trdng_md_cd', 'trdng_mthd_cd', 'bond_cd', 'bnds_nm', 'net_prc', 'yld_to_mrty', 'nmnl_vol', 'amnt', 'byr_instn_cn_full_nm', 'slr_instn_cn_full_nm'
    ]
    ndm_transaction_list = df_trade#[columns_to_export]
    return ndm_transaction_list

def get_mktPrice_data(date):
    # 将参数 `date` 动态地插入到 SQL 查询中
    # where mkt_data_upd_tm >= %s AND mkt_data_upd_tm <= %s
    date_start = f"{date} 00:00:00"
    date_end = f"{date} 23:59:59"
    sql = f"""
    select *
    from dpa.cbt_dl_mkt_info
    where dt_cnfrm = %s
    limit 3000
    """
    # 使用参数化查询执行 SQL
    df_trade = pg_select(sql, (date,))
    columns_to_export = [
        'dl_cd', 'trdng_md_cd', 'trdng_mthd_cd', 'bond_cd', 'bnds_nm', 'net_prc', 'yld_to_mrty', 'nmnl_vol', 'amnt', 'byr_instn_cn_full_nm', 'slr_instn_cn_full_nm'
    ]
    mktPrice_list = df_trade#[columns_to_export]
    return mktPrice_list

def get_instn_base_info(date):
    # 将参数 `date` 动态地插入到 SQL 查询中
    sql = f"""
    select *
    from dpa.rmb_hstry_actv_instn_base_info
    limit 300000
    """
    # 使用参数化查询执行 SQL
    df_trade = pg_select(sql, (date,))
    columns_to_export = [
        'dl_cd', 'trdng_md_cd', 'trdng_mthd_cd', 'bond_cd', 'bnds_nm', 'net_prc', 'yld_to_mrty', 'nmnl_vol', 'amnt', 'byr_instn_cn_full_nm', 'slr_instn_cn_full_nm'
    ]
    ndm_transaction_list = df_trade#[columns_to_export]
    return ndm_transaction_list

def get_broker_data(date, bond_id):
    # 将参数 `date` 格式化为 YYYY/MM/DD 以匹配 dl_tm 的格式
    date_start = f"{date} 00:00:00"
    date_end = f"{date} 23:59:59"

    # 构建 SQL 查询，将 bond_cd 和日期范围作为条件
    sql = f"""
    select * 
    from dpa.v_cbt_mny_brkrg_rltm_dl_non_cnex
    where dl_tm >= %s AND dl_tm <= %s AND bond_cd = %s
    limit 30000
    """
    # 使用参数化查询执行 SQL，传递开始时间、结束时间和债券ID
    df_trade = pg_select(sql, (date_start, date_end, bond_id))
    
    return df_trade

def get_transaction_data(date, bond_id):
    # 将参数 `bond_id` 添加到 SQL 查询中
    date_start = f"{date} 00:00:00"
    date_end = f"{date} 23:59:59"
    sql = f"""
    select *
    from dpa.cbt_dl_dtl
    where txn_dt >= %s AND txn_dt <= %s AND bond_cd = %s
    limit 100000
    """
    # 使用参数化查询执行 SQL，传递日期和债券ID
    df_trade = pg_select(sql, (date, bond_id))
    
    return df_trade

def get_valuation_data(date, bond_id):
    # 将参数 `bond_id` 添加到 SQL 查询中
    date_start = f"{date} 00:00:00"
    date_end = f"{date} 23:59:59"
    sql = f"""
    select *
    from dpa.cntrl_dpstry_vltn
    where vltn_dt >= %s AND vltn_dt <= %sAND bond_cd = %s
    limit 100000
    """
    # 使用参数化查询执行 SQL，传递日期和债券ID
    df_trade = pg_select(sql, (date, bond_id))
    
    return df_trade

# def get_broker_data(date, bond_id):
#     # 将参数 `date` 格式化为 YYYY/MM/DD 以匹配 dl_tm 的格式
#     date_start = f"{date} 00:00:00"
#     date_end = f"{date} 23:59:59"

#     # 构建 SQL 查询，将 bond_cd 和日期范围作为条件
#     sql = f"""
#     select * 
#     from dpa.v_cbt_mny_brkrg_rltm_dl_non_cnex
#     where dl_tm >= %s AND dl_tm <= %s AND bond_cd = %s
#     limit 30000
#     """
#     # 使用参数化查询执行 SQL，传递开始时间、结束时间和债券ID
#     df_trade = pg_select(sql, (date_start, date_end, bond_id))
    
#     return df_trade

# def get_transaction_data(date, bond_id):
#     # 将参数 `bond_id` 添加到 SQL 查询中
#     sql = f"""
#     select *
#     from dpa.cbt_dl_dtl
#     where txn_dt = %s AND bond_cd = %s
#     limit 100000
#     """
#     # 使用参数化查询执行 SQL，传递日期和债券ID
#     df_trade = pg_select(sql, (date, bond_id))
    
#     return df_trade

# def get_transaction_data(date, bond_id):
#     # 将参数 `bond_id` 添加到 SQL 查询中
#     sql = f"""
#     select *
#     from dpa.cbt_dl_dtl
#     where txn_dt = %s AND bond_cd = %s
#     limit 100000
#     """
#     # 使用参数化查询执行 SQL，传递日期和债券ID
#     df_trade = pg_select(sql, (date, bond_id))
    
#     return df_trade
