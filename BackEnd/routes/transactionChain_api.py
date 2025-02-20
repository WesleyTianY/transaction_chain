from flask import Blueprint, current_app, request, jsonify
import json
# import pandas as pd
# import networkx as nx
from backend.services.data_loader import load_data
# from backend.services.instnRelationGraph import generateGraphData
from backend.services.transaction_graph import construct_graph, calculate_degree, construct_graph
from backend.services.chain_project.chain_preprocess import preprocess_data, load_data_test, transactions_filter
from backend.services.chain_project.path_generating import create_directed_graph, find_all_paths
from backend.services.chain_project.path_linking import process_all_paths
from backend.services.chain_project.path_filtering import filter_subsets
transactionChain_bp = Blueprint('transactionChain', __name__)

def get_or_load_data(query_date):
    cache = current_app.config['cache']
    
    # Check if data is cached
    df_MarketPrice = cache.get('df_MarketPrice')
    df_transaction = cache.get('df_transaction')
    instn_base_info = cache.get('instn_base_info')
    df_chain_data = cache.get('df_chain_data')
    instn_dict = cache.get('instn_dict')
    cache = current_app.config['cache']
    query_date = cache.get('query_date')
    # If any of the data is not cached, load it and cache it
    if (df_MarketPrice is None or df_transaction is None or instn_base_info is None or df_chain_data is None or instn_dict is None or
        df_MarketPrice.empty or df_transaction.empty or instn_base_info.empty or df_chain_data.empty or not instn_dict):
        df_MarketPrice, df_transaction, instn_base_info, df_chain_data, instn_dict = load_data(query_date)
        cache.set('df_MarketPrice', df_MarketPrice)
        cache.set('df_transaction', df_transaction)
        cache.set('instn_base_info', instn_base_info)
        cache.set('df_chain_data', df_chain_data)
        cache.set('instn_dict', instn_dict)
    
    return df_MarketPrice, df_transaction, instn_base_info, df_chain_data, instn_dict

@transactionChain_bp.route('/get_transaction_chains', methods=['POST', 'GET'])
def get_transaction_chains():
    """
    Get sample transaction chains data.

    Returns:
    str: JSON formatted data.
    """
    # 获取 query_date 参数
    cache = current_app.config['cache']
    query_date = cache.get('query_date')
    if not query_date:
        return jsonify({"error": "query_date parameter is required"}), 400

    # 使用 query_date 加载数据
    _, _, _, df_chain_data, _ = get_or_load_data(query_date)

    # 构建图数据
    graph_data = construct_graph(df_chain_data)

    # 将图数据转换为 JSON 格式
    data_json = json.dumps(graph_data)
    
    return data_json

@transactionChain_bp.route('/get_transaction_chains_info', methods=['POST','GET'])
def process_transactions():
    """
    处理交易数据并返回过滤后的路径。

    Args:
    - file_path (str): 交易数据文件路径
    - inst_list (list): 机构名称列表

    Returns:
    - sorted_paths (list): 过滤后的路径列表
    """
    # inst_list = request.json.get('inst_list', [])
    inst_list = ['长线资本基金孙姣', '国金证券股份严佳', '华创证券有限马延威', '潍坊银行股份王梓涵', '鄂尔多斯银行郭宁', '粤开证券股份周荃', '交通银行股份何嘉隆', '华源证券股份钱淑雯']

    # 加载并预处理数据
    _, _, _, df_chain_data, _ = get_or_load_data()
    # df = load_data(file_path)
    merged_df = preprocess_data(df_chain_data)
    
    # 筛选并排序交易数据
    sorted_data = transactions_filter(merged_df, inst_list).sort_values(by='date_dl')

    # 创建有向图
    G_sorted_data = create_directed_graph(sorted_data)

    # 查找所有通路
    all_paths = find_all_paths(G_sorted_data, cutoff=10)

    # 处理路径组合
    the_connected_paths = process_all_paths(G_sorted_data, all_paths)

    # 过滤路径
    sorted_paths = filter_subsets(the_connected_paths)

    return jsonify(sorted_paths)
