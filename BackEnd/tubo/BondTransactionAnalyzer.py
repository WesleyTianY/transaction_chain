import pandas as pd
import numpy as np
from pathlib import Path

class BondTransactionAnalyzer:
    def __init__(self, config):
        # 初始化配置参数
        self.config = {
            "input_files": ["1.csv", "2.csv"],
            "result_folder": "chain_result2",
            "interest_rate_bond_threshold": 0.01,  # 利率债价差阈值
            "other_bond_threshold": 0.2,          # 非利率债价差阈值
            "profit_threshold": 5000,             # 盈利亏损阈值（万元）
            "remove_market_makers": False,
            "market_maker_list": "maker.csv",
            "required_columns": {
                "trade_id": "成交编号",
                "settlement_date": "结算日",
                "trade_time": "成交时间",
                "trade_type": "交易方式",
                "bond_type": "债券类型",
                "bond_name": "名称",
                "seller": "卖出方",
                "buyer": "买入方",
                "seller_trader": "卖出方交易员",
                "buyer_trader": "买入方交易员",
                "clean_price": "净价（元）",
                "yield": "到期收益率（%）",
                "nominal_amount": "券面总额（万元）",
                "settlement_amount": "结算金额（元）",
                "trade_date": "成交日"
            }
        }
        self.config.update(config)
        
        # 初始化数据容器
        self.all_transactions = None
        self.market_makers = set()
        
        # 创建结果目录
        Path(self.config["result_folder"]).mkdir(exist_ok=True)

    def load_data(self):
        """加载并预处理原始数据"""
        # 读取市场做市商名单
        if self.config["remove_market_makers"]:
            maker_df = pd.read_csv(self.config["market_maker_list"], encoding="GBK")
            self.market_makers = set(maker_df["机构名称"].values)
        
        # 加载交易数据
        dfs = []
        for f in self.config["input_files"]:
            try:
                df = pd.read_csv(f, encoding='utf-8')  # Try utf-8 first
            except UnicodeDecodeError:
                df = pd.read_csv(f, encoding='latin1')  # Fallback to latin1 encoding
            # df = pd.read_csv(f)
            dfs.append(df)
        
        # 合并并清理数据
        self.all_transactions = pd.concat(dfs).dropna()
        self._preprocess_data()
        
    def _preprocess_data(self):
        """数据预处理"""
        # 列重命名
        self.all_transactions.rename(columns={
            v: k for k, v in self.config["required_columns"].items()
        }, inplace=True)
        
        # 过滤有效交易类型
        valid_types = ['RFQ', 'Negotiate']
        self.all_transactions = self.all_transactions[
            self.all_transactions["trade_type"].isin(valid_types)
        ]
        
        # 转换日期格式
        self.all_transactions["trade_time"] = pd.to_datetime(
            self.all_transactions["trade_time"].str[:19]
        )
        self.all_transactions["trade_date"] = (
            self.all_transactions["trade_time"].dt.strftime("%Y%m%d")
        )
        
        # 过滤做市商交易
        if self.config["remove_market_makers"]:
            self.all_transactions = self.all_transactions[
                ~self.all_transactions["seller"].isin(self.market_makers) &
                ~self.all_transactions["buyer"].isin(self.market_makers)
            ]

    def analyze_transaction_chains(self):
        """主分析流程"""
        # 按结算日分组处理
        grouped = self.all_transactions.groupby("settlement_date")
        
        for date_str, daily_transactions in grouped:
            print(f"Processing {date_str}...")
            date_folder = Path(self.config["result_folder"]) / date_str
            date_folder.mkdir(exist_ok=True)
            
            # 按债券分组处理
            bond_groups = daily_transactions.groupby("bond_name")
            for bond_name, bond_transactions in bond_groups:
                self._process_bond_transactions(
                    bond_name, bond_transactions, date_folder
                )

    def _process_bond_transactions(self, bond_name, transactions, output_dir):
        """处理单只债券的交易"""
        # 确定价格阈值
        bond_type = transactions["bond_type"].iloc[0]
        price_threshold = (
            self.config["interest_rate_bond_threshold"] 
            if bond_type in ["国债", "政策性金融债"] 
            else self.config["other_bond_threshold"]
        )
        
        # 识别可疑机构
        suspicious_institutions = self._find_suspicious_institutions(transactions)
        if not suspicious_institutions:
            return
        
        # 合并相同交易对手的交易
        consolidated_transactions = self._consolidate_duplicate_trades(transactions)
        
        # 追踪交易链
        results = []
        for institution in suspicious_institutions:
            chain_results = self._trace_institution_chains(
                institution, consolidated_transactions, price_threshold
            )
            results.extend(chain_results)
        
        # 分批保存结果
        if results:
            output_path = output_dir / f"{bond_name}_results.csv"
            pd.DataFrame(results).to_csv(output_path, index=False)

    def _find_suspicious_institutions(self, transactions):
        """识别存在可疑净头寸的机构"""
        # 计算各机构的净交易量和损益
        buyers = transactions.groupby("buyer").agg({
            "nominal_amount": "sum",
            "settlement_amount": "sum"
        })
        sellers = transactions.groupby("seller").agg({
            "nominal_amount": "sum",
            "settlement_amount": "sum"
        })
        
        net_position = buyers.join(sellers, how="outer", lsuffix="_buy", rsuffix="_sell").fillna(0)
        net_position["net_amount"] = net_position["nominal_amount_sell"] - net_position["nominal_amount_buy"]
        net_position["net_profit"] = net_position["settlement_amount_sell"] - net_position["settlement_amount_buy"]
        
        # 筛选可疑机构
        threshold = self.config["profit_threshold"] * 10000  # 转换为元
        suspicious = net_position[
            (abs(net_position["net_profit"]) > threshold) &
            (net_position["net_amount"] != 0)
        ].index.tolist()
        
        return suspicious

    def _consolidate_duplicate_trades(self, transactions):
        """合并相同交易对手的重复交易"""
        group_keys = ["seller", "buyer", "seller_trader", "buyer_trader", "yield"]
        grouped = transactions.groupby(group_keys)
        
        consolidated = []
        for (seller, buyer, s_trader, b_trader, yld), group in grouped:
            if len(group) > 1:
                combined = pd.Series({
                    "trade_id": "|".join(group["trade_id"]),
                    "nominal_amount": group["nominal_amount"].sum(),
                    "settlement_amount": group["settlement_amount"].sum(),
                    "clean_price": group["clean_price"].mean(),
                    **dict(zip(group_keys, [seller, buyer, s_trader, b_trader, yld]))
                })
                consolidated.append(combined)
            else:
                consolidated.append(group.iloc[0])
        
        return pd.DataFrame(consolidated)

    def _trace_institution_chains(self, institution, transactions, price_threshold):
        """追踪单个机构的交易链条"""
        # 正向追踪（上游）
        upstream_chains = self._trace_transaction_chain(
            institution, transactions, direction="upstream", 
            price_threshold=price_threshold
        )
        
        # 反向追踪（下游）
        downstream_chains = self._trace_transaction_chain(
            institution, transactions, direction="downstream",
            price_threshold=price_threshold
        )
        
        # 合并并分析链条
        combined_chains = self._analyze_combined_chains(
            upstream_chains, downstream_chains, institution
        )
        
        return combined_chains

    def _trace_transaction_chain(self, start_institution, transactions, 
                                direction="upstream", price_threshold=0.1):
        """追踪单个方向的交易链"""
        # 实现核心的链条追踪逻辑（此处需要根据原代码逻辑补充实现细节）
        # 返回追踪到的交易链信息
        return []  # 示例返回

    def _analyze_combined_chains(self, upstream, downstream, institution):
        """分析合并后的交易链条"""
        # 实现链条合并和损益计算逻辑
        return []  # 示例返回

# 使用示例
if __name__ == "__main__":
    config = {
        "input_files": ["random_bond_transactions.csv"],
        "result_folder": "results",
        "profit_threshold": 5000  # 万元
    }
    
    analyzer = BondTransactionAnalyzer(config)
    analyzer.load_data()
    analyzer.analyze_transaction_chains()
