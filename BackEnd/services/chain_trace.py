import pandas as pd
import numpy as np
from collections import defaultdict
import pandas as pd

# 配置参数
CONFIG = {
    "columns": {
        "trade_id": 'dl_cd',
        "trade_time": "dl_tm",
        'amnt':'amnt',
        'acrd_intrst':'acrd_intrst',
        "trade_date": 'txn_dt',
        "settle_date": "stlmnt_dt",
        "nmnl_vol": 'nmnl_vol',  # Or nmnl_vol depending on the field
        "seller": "byr_trd_acnt_cn_shrt_nm",  # Could be different depending on the data
        "buyer": "slr_trd_acnt_cn_shrt_nm",  # Could be different depending on the data
        "seller_trader": "byr_trdr_nm",  # 买方交易员
        "buyer_trader": "slr_trdr_nm",  # 卖方交易员
        "price": "net_prc",  # 净价（元）
        "yield": 'yld_to_mrty',  # 到期收益率（%）
        "trade_method": "trdng_mthd_cd",  # 交易方式
        "bond_name": "bnds_nm",  # 债券名称
    },
    "date_format": "%Y-%m-%d",
    "datetime_format": "%Y/%m/%d",
    "datetime_format_full": "%Y-%m-%d hh:mm:ss",
    
    # 业务参数
    "find_threshold_rate_bond": 0.01,
    "find_threshold_other_bond": 0.2,
    "profit_loss_threshold": 5000,
    "remove_market_maker": True,
    "save_directory": "chain_result2",
    "market_price_threshold": 0.05,
    "price_ratio_min": 0.015,
    "single_price_boundary_min": 2,
    "target_price_ratio_min": 0.05,
    "path_length": 3
}

# 读取所有交易数据
def read_trade_data():
    """
    读取多个 CSV 文件并合并为一个 DataFrame。
    """
    data_df = pd.read_csv("./static/bond_dtl_10_08.csv")
    data_df.drop("Unnamed: 0", axis=1, inplace=True)
    data_df = data_df.reset_index(drop=True)
    return data_df

# 处理时间和日期字段
def process_time_and_date(all_trade_data):
    """
    处理交易时间和结算日期。
    """
    # 交易时间列：转换为 datetime 类型
    all_trade_data[CONFIG["columns"]["trade_time"]] = pd.to_datetime(
        all_trade_data[CONFIG["columns"]["trade_time"]].str[:19], format="%Y-%m-%d %H:%M:%S"
    )
    return all_trade_data

def select_and_rename_all_columns(all_trade_data):
    """
    提取和重命名所有指定的列。
    """
    selected_columns = {value: key for key, value in CONFIG["columns"].items()}
    return all_trade_data[list(selected_columns.keys())]

# 过滤交易方式
def filter_trade_method(all_trade_data):
    """
    过滤只保留 'RFQ' 或 'Negotiate' 方式的交易。
    """
    return all_trade_data[all_trade_data[CONFIG["columns"]["trade_method"]].isin(['RFQ', 'Negotiate'])]

def filter_strange_trade(df, threshold=0.1):
    """
    筛选偏离度较高的交易，偏离度基于 buyer 自身的市场价格。

    参数：
        df (pd.DataFrame): 包含交易数据的 DataFrame。
        threshold (float): 偏离度的阈值，默认是 10% (0.1)。

    返回：
        pd.DataFrame: 包含偏离度超过阈值的异常交易。
    """
    # 生成市场价格映射
    market_price_mapping = df.groupby(CONFIG["columns"]["buyer"])[CONFIG["columns"]["price"]].mean().to_dict()

    # 映射市场价格
    df['market_price'] = df[CONFIG["columns"]["buyer"]].map(market_price_mapping)

    # 计算价格偏离度
    df['price_dev'] = (df[CONFIG["columns"]["price"]] - df['market_price']) / df['market_price']

    # 筛选偏离度超出指定阈值的交易
    abnormal_trades = df[(df['price_dev'] > threshold) | (df['price_dev'] < -threshold)]

    return abnormal_trades

# 主函数：读取和处理交易数据
def main():
    # 读取数据
    all_trade_data = read_trade_data()
    
    # 处理时间和日期
    all_trade_data = process_time_and_date(all_trade_data)
    
    # 过滤交易方式
    all_trade_data = filter_trade_method(all_trade_data)
    
    # 提取和重命名列
    all_trade_data = select_and_rename_all_columns(all_trade_data)

    return all_trade_data

# 获取金额组合和对应的交易索引
def get_amount_dict(transaction_indices, trade_data):
    """
    根据交易索引获取金额组合和对应的交易索引。
    
    参数:
        transaction_indices (list): 交易索引列表。
        trade_data (pd.DataFrame): 包含交易数据的 DataFrame。
    
    返回:
        dict: 以金额为键，交易索引集合为值的字典。
    """
    amount_dict = defaultdict(set)
    if not set(transaction_indices).issubset(set(trade_data.index)):
        raise ValueError("Some indices in transaction_indices are not valid.")

    for idx in transaction_indices:
        amt = trade_data.at[idx, CONFIG["columns"]["amnt"]]
        amount_dict[amt].add(idx)
    return amount_dict

# 根据方向选择交易链的下一步
def choose_next_edge(index, amt, trade_data, direction):
    """
    根据方向选择交易链的下一步。
    
    参数:
        index (int): 当前交易的索引。
        amt (float): 当前交易的金额。
        trade_data (pd.DataFrame): 包含交易数据的 DataFrame。
        direction (str): 追踪方向，"forward" 或 "backward"。
    
    返回:
        list: 下一步交易的索引列表。
    """
    seller_col = CONFIG["columns"]["seller"]
    buyer_col = CONFIG["columns"]["buyer"]

    if direction == "forward":  # 正向选择
        condition = (
            (trade_data[CONFIG["columns"]["amnt"]] == amt) & 
            (trade_data[seller_col] == trade_data.at[index, buyer_col])
        )
    elif direction == "backward":  # 反向选择
        condition = (
            (trade_data[CONFIG["columns"]["amnt"]] == amt) & 
            (trade_data[buyer_col] == trade_data.at[index, seller_col])
        )
    else:
        raise ValueError("Invalid direction. Use 'forward' or 'backward'.")

    return trade_data[condition].index.tolist()

# 追踪交易链（迭代版）
def trace_trade_chains_iterative(trade_data, start_inst, direction, max_depth=5):
    """
    追踪交易链，使用迭代方式，避免递归限制。
    """
    stack = [(start_inst, 0, [])]  # (当前机构, 当前深度, 当前路径)
    all_paths = []
    all_path_ids = []

    while stack:
        current_inst, depth, current_path = stack.pop()
        if depth > max_depth:
            continue

        # 添加当前机构到路径
        current_path = current_path + [current_inst]

        # 找到相关交易
        related_trades = (trade_data[trade_data['卖方'] == current_inst]
                          if direction == "f" else trade_data[trade_data['买方'] == current_inst])

        if related_trades.empty:
            all_paths.append(current_path)
            continue

        for idx, trade in related_trades.iterrows():
            next_inst = trade['买方'] if direction == "f" else trade['卖方']
            stack.append((next_inst, depth + 1, current_path))
            all_path_ids.append(trade['交易编号'])

    return all_paths, all_path_ids

# 递归追踪交易链
def trace_trade_chains(trade_data, current_inst, direction, path=None, path_ids=None, max_depth=5):
    """
    递归追踪交易链。
    
    参数:
        trade_data (pd.DataFrame): 包含交易数据的 DataFrame。
        current_inst (str): 当前机构。
        direction (str): "forward" 或 "backward"。
        path (list): 当前路径。
        path_ids (list): 当前路径中的交易 ID。
        max_depth (int): 最大递归深度。

    返回:
        tuple: 路径 (list) 和路径中的交易 ID (list)。
    """
    if path is None:
        path = []
    if path_ids is None:
        path_ids = []
    
    path.append(current_inst)  # 添加当前机构到路径

    # 检查递归深度
    if len(path) >= max_depth:
        return path, path_ids

    seller_col = CONFIG["columns"]["seller"]
    buyer_col = CONFIG["columns"]["buyer"]
    trade_id_col = CONFIG["columns"]["trade_id"]

    if direction == "forward":
        relevant_trades = trade_data[trade_data[seller_col] == current_inst]
    elif direction == "backward":
        relevant_trades = trade_data[trade_data[buyer_col] == current_inst]
    else:
        raise ValueError("Invalid direction. Use 'forward' or 'backward'.")

    if relevant_trades.empty:  # 如果没有相关交易，结束递归
        return path, path_ids

    all_paths = []
    for idx, trade in relevant_trades.iterrows():
        next_inst = trade[buyer_col] if direction == "forward" else trade[seller_col]
        sub_path, sub_path_ids = trace_trade_chains(
            trade_data, next_inst, direction, path.copy(), path_ids.copy(), max_depth
        )
        sub_path_ids.append(trade[trade_id_col])  # 添加当前交易 ID
        all_paths.append((sub_path, sub_path_ids))

    # 返回最长路径 (可根据业务需求更改逻辑)
    longest_path = max(all_paths, key=lambda x: len(x[0]))
    return longest_path

# 双向追踪交易链
def trace_trade_chains_bidirection(trade_data, start_inst, max_depth=5):
    """
    双向追踪交易链。
    
    参数:
        trade_data (pd.DataFrame): 包含交易数据的 DataFrame。
        start_inst (str): 起始机构。
        max_depth (int): 最大递归深度。

    返回:
        dict: 包含正向和反向路径及对应交易 ID 的字典。
    """
    reverse_path, reverse_path_ids = trace_trade_chains(
        trade_data, start_inst, direction="backward", max_depth=max_depth
    )
    reverse_path = reverse_path[::-1]  # 反转路径，使其从起始机构向后排列

    forward_path, forward_path_ids = trace_trade_chains(
        trade_data, start_inst, direction="forward", max_depth=max_depth
    )
    
    combined_path = reverse_path[:-1] + forward_path  # 合并路径，去掉重复的中间节点
    combined_path_ids = reverse_path_ids + forward_path_ids

    return {
        "path": combined_path,
        "path_ids": combined_path_ids
    }

### 测试整合
# if __name__ == "__main__":
#     # 假设 main() 加载交易数据

#     df = main()

#     # 测试起始机构
#     start_institution = "机构A"

#     # 单向追踪
#     forward_chain = trace_trade_chains(df, current_inst=start_institution, direction="forward", max_depth=5)
#     backward_chain = trace_trade_chains(df, current_inst=start_institution, direction="backward", max_depth=5)

#     print("Forward Chain:", forward_chain)
#     print("Backward Chain:", backward_chain)

#     # 双向追踪
#     bidirectional_chain = trace_trade_chains_bidirection(df, start_inst=start_institution, max_depth=5)
#     print("Bidirectional Chain:", bidirectional_chain)
