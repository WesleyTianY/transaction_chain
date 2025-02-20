import os
import pandas as pd
from datetime import datetime
import math
import json

# 定义temp文件夹路径和队列文件路径
TEMP_DIR = 'backend/services/static/temp'
QUEUE_FILE = os.path.join(TEMP_DIR, 'date_queue.json')
os.makedirs(TEMP_DIR, exist_ok=True)  # 如果文件夹不存在，则创建
MAX_DATES = 10  # 最大保留日期文件夹数

def maintain_date_queue(query_date):
    # 如果队列文件存在，读取现有队列
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            date_queue = json.load(f)
    else:
        date_queue = []

    # 更新队列：如果日期不在队列中，添加新日期到队列尾部
    if query_date not in date_queue:
        date_queue.append(query_date)

    # 如果队列长度超过最大限制，删除最旧的日期
    if len(date_queue) > MAX_DATES:
        oldest_date = date_queue.pop(0)
        oldest_date_dir = os.path.join(TEMP_DIR, oldest_date)
        if os.path.exists(oldest_date_dir):
            # 删除最旧日期的文件夹
            for file in os.listdir(oldest_date_dir):
                os.remove(os.path.join(oldest_date_dir, file))
            os.rmdir(oldest_date_dir)

    # 将更新后的队列写回文件
    with open(QUEUE_FILE, 'w') as f:
        json.dump(date_queue, f)

def load_data_data_center(query_date):
    from backend.services.data_center import get_transaction_data, get_valuation_data, get_broker_data, get_instn_base_info
    try:
        # 创建日期文件夹路径
        date_dir = os.path.join(TEMP_DIR, query_date)
        os.makedirs(date_dir, exist_ok=True)  # 如果文件夹不存在，则创建

        # 定义每个文件的完整路径
        file_transaction = os.path.join(date_dir, f'transaction_{query_date}.csv')
        file_valuation = os.path.join(date_dir, f'valuation_{query_date}.csv')
        file_broker = os.path.join(date_dir, f'broker_{query_date}.csv')
        file_instn_base_info = os.path.join(date_dir, f'instn_base_info_{query_date}.csv')

        # 检查文件是否存在，如果存在则直接从本地读取数据
        if all(os.path.exists(file) for file in [file_transaction, file_valuation, file_broker, file_instn_base_info]):
            print("数据文件已存在，直接从本地读取")
            df_transaction = pd.read_csv(file_transaction)
            df_valuation = pd.read_csv(file_valuation)
            df_broker_data = pd.read_csv(file_broker)
            instn_base_info = pd.read_csv(file_instn_base_info)
        else:
            # 从数据库获取数据
            print("数据文件不存在或日期不匹配，从数据库下载")
            df_transaction = get_transaction_data(query_date)
            df_valuation = get_valuation_data(query_date)
            df_broker_data = get_broker_data(query_date)
            instn_base_info = get_instn_base_info(query_date)
            
            # 保存数据到本地CSV文件
            df_transaction.to_csv(file_transaction, index=False)
            df_valuation.to_csv(file_valuation, index=False)
            df_broker_data.to_csv(file_broker, index=False)
            instn_base_info.to_csv(file_instn_base_info, index=False)

            df_transaction = pd.read_csv(file_transaction, dtype={'bond_cd': str})
            df_valuation = pd.read_csv(file_valuation)
            df_broker_data = pd.read_csv(file_broker)
            instn_base_info = pd.read_csv(file_instn_base_info)
        # 更新日期队列
        maintain_date_queue(query_date)

        # 转换时间戳列
        df_valuation['timeStamp'] = pd.to_datetime(df_valuation['vltn_dt'], errors='coerce').dt.tz_localize(None)
        df_transaction['timeStamp'] = pd.to_datetime(df_transaction['dl_tm'], errors='coerce').dt.tz_localize(None)
        
        # 加载链数据
        df_chain_data = pd.read_csv('backend/services/static/bond_2005496_2006_2402.csv')

        # 处理字典
        instn_dict = _prepare_instn_dict(instn_base_info)

        return df_broker_data, df_transaction, df_valuation, instn_base_info, df_chain_data, instn_dict

    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None, None, None

def _prepare_instn_dict(instn_base_info):
    selected_cols = ['instn_cd', 'instn_tp', 'instn_cn_full_nm']
    result_df = instn_base_info[selected_cols]
    instn_dict = result_df.set_index('instn_cd').to_dict(orient='index')
    for key, value in instn_dict.items():
        for sub_key, sub_val in value.items():
            if isinstance(sub_val, float) and math.isnan(sub_val):
                instn_dict[key][sub_key] = None
    return instn_dict

def load_data_data_center1(query_date):
    from backend.services.data_center import get_transaction_data, get_mktPrice_data, get_valuation_data, get_instn_base_info, get_broker_data
    try:
        # 加载数据
        df_transaction = get_transaction_data(query_date)
        df_valuation = get_valuation_data(query_date)
        df_broker_data = get_broker_data(query_date)
        
        # 转换时间戳列
        df_valuation['timeStamp'] = pd.to_datetime(df_valuation['vltn_dt'], errors='coerce').dt.tz_localize(None)
        df_transaction['timeStamp'] = pd.to_datetime(df_transaction['dl_tm'], errors='coerce').dt.tz_localize(None)
        
        # 加载静态文件
        instn_base_info = pd.read_csv('backend/services/static/rmb_hstry_actv_instn_base_info.csv')
        # 加载链数据
        df_chain_data = pd.read_csv('backend/services/static/bond_2005496_2006_2402.csv')

        # 处理字典
        instn_dict = _prepare_instn_dict(instn_base_info)

        return df_broker_data, df_transaction, df_valuation, instn_base_info, df_chain_data, instn_dict

    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None, None, None

def load_data_local(query_date):
    """
    Load data from the CSV files.

    Returns:
    tuple: Tuple containing DataFrames for MarketPrice, transaction, and instn_base_info.
    """
    # Load the data from the CSV files
    # df_MarketPrice = pd.read_csv('backend/services/static/mkt_price_list_all_20230705.csv')
    # df_transaction = pd.read_csv('backend/services/static/ndm_transaction_list_all_20230705.csv')
    df_MarketPrice = pd.read_csv('backend/services/static/bond_brk10_08.csv', dtype={'bond_cd': str})
    df_transaction = pd.read_csv('backend/services/static/bond_dtl_10_08.csv')
    df_valuation = pd.read_csv('backend/services/static/bond_2024_10_09_valuation.csv')
    # 只抽取10月8日的信息
    df_valuation['timeStamp'] = pd.to_datetime(df_valuation['vltn_dt']).dt.tz_localize(None)
    df_transaction['timeStamp'] = pd.to_datetime(df_transaction['dl_tm']).dt.tz_localize(None)
    df_transaction = df_transaction[df_transaction['timeStamp'].dt.date == pd.to_datetime('2024-10-09').date()]
    # df_transaction = df_transaction.sort_values(by='timeStamp', ascending=True)

    instn_base_info = pd.read_csv('backend/services/static/rmb_hstry_actv_instn_base_info.csv')
    header_string = "dl_cd,txn_dt,dl_tm,bsns_tm,bond_cd,bnds_nm,net_prc,yld_to_mrty,nmnl_vol,amnt,acrd_intrst,totl_acrd_intrst,all_prc,stlmnt_amnt,stlmnt_dt,ttm_yrly,byr_qt_cd,byr_instn_cd,byr_cfets_instn_cd,byr_instn_cn_full_nm,byr_instn_cn_shrt_nm,byr_instn_en_shrt_nm,byr_trdr_nm,byr_adrs,byr_trdr_fax,byr_lgl_rprsntv,byr_trdr_tel,buy_side_trdng_acnt_cd,byr_cptl_bnk_nm,byr_cptl_acnt_no,byr_pymnt_sys_cd,byr_dpst_acnt_nm,buy_side_dpst_cd,byr_trd_acnt_cfets_cd,byr_trd_acnt_cn_full_nm,byr_trd_acnt_cn_shrt_nm,byr_trd_acnt_en_shrt_nm,byr_cptl_acnt_nm,byr_trd_acnt_en_full_nm,slr_qt_cd,slr_instn_cd,slr_cfets_instn_cd,slr_instn_cn_full_nm,slr_instn_cn_shrt_nm,slr_instn_en_shrt_nm,slr_trdr_cd,slr_trdr_nm,slr_adrs,slr_trdr_fax,slr_lgl_rprsntv,slr_trdr_tel,sell_side_trdng_acnt_cd,slr_cptl_bnk_nm,slr_cptl_acnt_no,slr_pymnt_sys_cd,slr_dpst_acnt_nm,sell_side_dpst_acnt,slr_trd_acnt_cfets_cd,slr_trd_acnt_cn_full_nm,slr_trd_acnt_cn_shrt_nm,slr_trd_acnt_en_shrt_nm,slr_cptl_acnt_nm,slr_trd_acnt_en_full_nm,crt_tm,upd_tm"
    header_list = header_string.split(',')
    # df_chain_data = pd.read_csv('backend/services/static/ndm_transaction_list_all_20230705.csv', usecols=header_list)
    df_chain_data = pd.read_csv('backend/services/static/bond_2005496_2006_2402.csv', usecols=header_list)
    # Convert DataFrame to dictionary
    instn_dict = _prepare_instn_dict(instn_base_info)

    return df_MarketPrice, df_transaction, df_valuation, instn_base_info, df_chain_data, instn_dict

def _prepare_instn_dict(instn_base_info):
    selected_cols = ['instn_cd', 'instn_tp', 'instn_cn_full_nm']
    result_df = instn_base_info[selected_cols]
    instn_dict = result_df.set_index('instn_cd').to_dict(orient='index')
    for key, value in instn_dict.items():
        for sub_key, sub_val in value.items():
            if isinstance(sub_val, float) and math.isnan(sub_val):
                instn_dict[key][sub_key] = None
    return instn_dict

def load_data(query_date):
    """
    Determine which data loader function to use based on the environment.
    """
    mode = os.getenv('FLASK_CONFIG', 'local')
    if mode == 'prod':
        return load_data_data_center(query_date)
    else:
        return load_data_local(query_date)

