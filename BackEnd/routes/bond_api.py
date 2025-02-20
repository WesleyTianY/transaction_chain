import json
import os
import numpy as np
import pandas as pd
from flask import Blueprint, current_app, jsonify, request

# from backend.services.sql import pg_select
bond_bp = Blueprint('bond', __name__)

def load_data_data_center(query_date, bond_id):
    """
    Load and filter data from the data center (production environment).
    """
    from backend.services.data_center import get_transaction_data, get_valuation_data, get_broker_data

    # 加载并直接筛选数据
    broker_data = get_broker_data(query_date, bond_id)
    ndm_transaction_data = get_transaction_data(query_date, bond_id)
    valuation_data = get_valuation_data(query_date, bond_id)

    return broker_data, ndm_transaction_data, valuation_data

def load_data_local(query_date, bond_id):
    """
    Load and filter data from local CSV files.
    """
    # 加载本地 CSV 文件
    df_mkt = pd.read_csv('backend/services/static/bond_brk10_08.csv', low_memory=False, dtype={'bondcd': str})
    ndm_transaction_data = pd.read_csv('backend/services/static/bond_dtl_10_08.csv', low_memory=False, dtype={'bondcd': str})
    valuation_data = pd.read_csv('backend/services/static/bond_2024_10_09_valuation.csv', low_memory=False, dtype={'bondcd': str})
    
    # 转换 selected_date 为日期类型
    selected_date = pd.to_datetime(query_date)
    
    # 筛选数据
    df_mkt_filtered = df_mkt[(df_mkt['bond_cd'] == int(bond_id)) & 
                             (pd.to_datetime(df_mkt['dl_tm']).dt.date == selected_date.date())].copy()
    ndm_transaction_filtered = ndm_transaction_data[(ndm_transaction_data['bond_cd'] == bond_id) & 
                                                    (pd.to_datetime(ndm_transaction_data['dl_tm']).dt.date == selected_date.date())].copy()
    valuation_filtered = valuation_data[valuation_data['bond_cd'] == bond_id].copy()
    
    return df_mkt_filtered, ndm_transaction_filtered, valuation_filtered

def load_data(query_date, bond_id):
    """
    Determine which data loader function to use based on the environment.
    """
    mode = os.getenv('FLASK_CONFIG', 'local')
    if mode == 'prod':
        return load_data_data_center(query_date, bond_id)
    else:
        return load_data_local(query_date, bond_id)

@bond_bp.route('/bondData', methods=['POST', 'GET'])
def data():
    bond_id = request.args.get('BondId')  # 获取债券ID
    selected_date = request.args.get('selectedDate')  # 获取选择的日期
    selected_date = '2024-10-08'
    print("BondId:", bond_id)
    print("selectedDate:", selected_date)

    # 从数据库读取并过滤数据
    df_mkt_filtered_data, ndm_transaction_sorted_data, valuation_filtered_data = load_data(selected_date, bond_id)

    # 转换时间戳格式并去除时区信息
    df_mkt_filtered_data['timeStamp'] = pd.to_datetime(df_mkt_filtered_data['dl_tm']).dt.tz_localize(None)
    mean_dlt_prc = df_mkt_filtered_data['dlt_prc'].astype(float).mean()
    std_dlt_prc = df_mkt_filtered_data['dlt_prc'].astype(float).std()

    # 剔除偏离均值10个标准差之外的数据
    df_mkt_filtered_data = df_mkt_filtered_data[np.abs(df_mkt_filtered_data['dlt_prc'].astype(float) - mean_dlt_prc) <= 10 * std_dlt_prc]

    # 排序
    df_mkt_filtered_data = df_mkt_filtered_data.sort_values(by='timeStamp', ascending=True)
    ndm_transaction_sorted_data['timeStamp'] = pd.to_datetime(ndm_transaction_sorted_data['dl_tm']).dt.tz_localize(None)
    ndm_transaction_sorted_data = ndm_transaction_sorted_data.sort_values(by='timeStamp', ascending=True)

    # 获取债券名称
    bnds_nm = ndm_transaction_sorted_data["bnds_nm"].unique()[0]

    # 设置随机种子以便重现
    np.random.seed(42)
    transaction_types = np.random.choice(['NDM', 'RFQ', 'QDM'], size=len(ndm_transaction_sorted_data), p=[0.2, 0.5, 0.3])
    ndm_transaction_sorted_data['transaction_type'] = transaction_types

    # 构建响应数据
    data = {
        "bond_cd": str(bond_id),
        "time": str(selected_date),
        "bnds_nm": str(bnds_nm),
        "broker_data": [
            {
                "timeStamp": str(row['timeStamp']),
                "dlt_prc": str(row['dlt_prc'])
            }
            for _, row in df_mkt_filtered_data.iterrows()
        ],
        "transaction_data": [
            {
                "timeStamp": str(row['timeStamp']),
                "nmnl_vol": str(row['nmnl_vol']),
                "yld_to_mrty": str(row['yld_to_mrty']),
                "bond_cd": str(row['bond_cd']),
                "transactionId": str(row['dl_cd']),
                "netPrice": str(row['net_prc']),
                "transactionVolume": str(row['nmnl_vol']),
                "byr_instn_cn_full_nm": str(row['byr_trd_acnt_cn_shrt_nm']),
                "slr_instn_cn_full_nm": str(row['slr_trd_acnt_cn_shrt_nm']),
                "byr_instn_cd": str(row['byr_instn_cd']),
                "slr_instn_cd": str(row['slr_instn_cd']),
                "byr_trdr_nm": str(row['byr_trdr_nm']),
                "slr_trdr_nm": str(row['slr_trdr_nm']),
                "transaction_type": str(row['trdng_md_cd']),
                "dl_tp": str(row["dl_tp"])
            }
            for _, row in ndm_transaction_sorted_data.iterrows()
        ],
        "val_data": [
            {
                "timeStamp": str(row['vltn_dt']),
                "vltn_net_prc": str(row['vltn_net_prc']),
                "yld_to_mrty": str(row['yld_to_mrty'])
            }
            for _, row in valuation_filtered_data.iterrows()
        ]
    }

    return jsonify(data)
