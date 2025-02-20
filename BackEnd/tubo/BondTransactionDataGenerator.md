import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class BondTransactionDataGenerator:
    def __init__(self, config):
        self.config = {
            "num_transactions": 1000,  # 生成的交易数量
            "start_date": "2023-01-01",  # 起始日期
            "end_date": "2023-12-31",  # 结束日期
            "institutions": ["机构A", "机构B", "机构C", "机构D", "机构E"],  # 参与机构
            "traders": ["交易员1", "交易员2", "交易员3", "交易员4", "交易员5"],  # 交易员
            "bond_types": ["国债", "政策性金融债", "企业债"],  # 债券类型
            "bond_names": ["债券A", "债券B", "债券C", "债券D", "债券E"],  # 债券名称
            "price_range": (95, 105),  # 价格范围（净价）
            "yield_range": (2.5, 5.0),  # 收益率范围
            "nominal_amount_range": (1000, 10000),  # 券面总额范围（万元）
            "trade_types": ["RFQ", "Negotiate"],  # 交易方式
            "output_file": "random_bond_transactions.csv"  # 输出文件名
        }
        self.config.update(config)

    def generate_random_date(self, start_date, end_date):
        """生成随机日期"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        delta = end - start
        random_days = random.randint(0, delta.days)
        return start + timedelta(days=random_days)

    def generate_random_transaction(self):
        """生成单笔随机交易"""
        trade_id = f"TR{random.randint(100000, 999999)}"  # 交易编号
        trade_date = self.generate_random_date(
            self.config["start_date"], self.config["end_date"]
        )
        trade_time = trade_date + timedelta(
            hours=random.randint(9, 16),  # 交易时间在9:00-16:00之间
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        trade_type = random.choice(self.config["trade_types"])  # 交易方式
        bond_type = random.choice(self.config["bond_types"])  # 债券类型
        bond_name = random.choice(self.config["bond_names"])  # 债券名称
        seller, buyer = random.sample(self.config["institutions"], 2)  # 买卖双方
        seller_trader = random.choice(self.config["traders"])  # 卖方交易员
        buyer_trader = random.choice(self.config["traders"])  # 买方交易员
        clean_price = round(random.uniform(*self.config["price_range"]), 2)  # 净价
        yield_rate = round(random.uniform(*self.config["yield_range"]), 2)  # 收益率
        nominal_amount = random.randint(*self.config["nominal_amount_range"])  # 券面总额
        settlement_amount = round(nominal_amount * clean_price / 100, 2)  # 结算金额

        return {
            "成交编号": trade_id,
            "成交日期": trade_date.strftime("%Y-%m-%d"),
            "成交时间": trade_time.strftime("%Y-%m-%d %H:%M:%S"),
            "交易方式": trade_type,
            "债券类型": bond_type,
            "名称": bond_name,
            "卖出方": seller,
            "卖出方交易员": seller_trader,
            "买入方": buyer,
            "买入方交易员": buyer_trader,
            "净价（元）": clean_price,
            "到期收益率（%）": yield_rate,
            "券面总额（万元）": nominal_amount,
            "交易金额（元）": settlement_amount,
            "结算日": trade_date.strftime("%Y-%m-%d"),
            "结算金额（元）": settlement_amount
        }

    def generate_data(self):
        """生成随机交易数据"""
        transactions = []
        for _ in range(self.config["num_transactions"]):
            transactions.append(self.generate_random_transaction())
        
        df = pd.DataFrame(transactions)
        df.to_csv(self.config["output_file"], index=False, encoding="GBK")
        print(f"随机交易数据已生成并保存到 {self.config['output_file']}")

# 使用示例
if __name__ == "__main__":
    config = {
        "num_transactions": 5000,  # 生成5000笔交易
        "output_file": "random_bond_transactions.csv"  # 保存文件名
    }
    
    generator = BondTransactionDataGenerator(config)
    generator.generate_data()
