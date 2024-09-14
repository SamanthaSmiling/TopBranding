import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)

NUM_RECORDS = 10000  # 生成的记录数
NUM_ITEMS = 300  # 商品数量
NUM_SELLERS = 200  # 商家数量
NUM_BRANDS = 20  # 品牌数量
NUM_SECTORS = 8  # 一级类目数量
NUM_CATEGORIES = 20  # 二级类目数量

# 唯一18位随机数
transaction_ids = [''.join(random.choices('0123456789', k=18)) for _ in range(NUM_RECORDS)]

# Item 1 - Item 300
item_names = [f"Item {i+1}" for i in range(NUM_ITEMS)]
items = np.random.choice(item_names, size=NUM_RECORDS)

# Seller 1 - Seller 200
seller_names = [f"Seller {i+1}" for i in range(NUM_SELLERS)]
sellers = np.random.choice(seller_names, size=NUM_RECORDS)

# Brand 1 - Brand 20，泊松分布
brand_names = [f"Brand {i+1}" for i in range(NUM_BRANDS)]
brand_probs = np.random.poisson(lam=1, size=NUM_BRANDS) + 1  # 防止概率为零
brand_probs = brand_probs / brand_probs.sum()  # 归一化概率
brands = np.random.choice(brand_names, size=NUM_RECORDS, p=brand_probs)

# Sector 1 - Sector 30，正态分布
sector_names = [f"Sector {i+1}" for i in range(NUM_SECTORS)]
sector_probs = np.random.normal(loc=0, scale=1, size=NUM_SECTORS)
sector_probs = np.abs(sector_probs)  # 取正值
sector_probs = sector_probs / sector_probs.sum()  # 归一化概率
sectors = np.random.choice(sector_names, size=NUM_RECORDS, p=sector_probs)

# Cata 1 - Cata 100，按正态分布生成
category_names = [f"Cata {i+1}" for i in range(NUM_CATEGORIES)]
category_probs = np.random.normal(loc=0, scale=1, size=NUM_CATEGORIES)
category_probs = np.abs(category_probs)  # 取正值
category_probs = category_probs / category_probs.sum()  # 归一化概率
categories = np.random.choice(category_names, size=NUM_RECORDS, p=category_probs)

# 12位随机数，可重复
user_ids = [''.join(random.choices('0123456789', k=12)) for _ in range(NUM_RECORDS)]

# 正态分布，均值10000，方差5000
transaction_amounts = np.random.normal(loc=10000, scale=5000, size=NUM_RECORDS)
transaction_amounts = np.clip(transaction_amounts, 0, 50000)  # 保证大于0，小于50000

# 正态分布，均值5500，方差500
unit_prices = np.random.normal(loc=5500, scale=500, size=NUM_RECORDS)
unit_prices = np.clip(unit_prices, 0, 30000)  # 保证大于0，小于30000

# 2022.01.01 - 2024.08.31之间随机日期
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 8, 31)
date_range = (end_date - start_date).days
transaction_dates = [start_date + timedelta(days=random.randint(0, date_range)) for _ in range(NUM_RECORDS)]


df = pd.DataFrame({
    'Transaction ID': transaction_ids,
    'Item Name': items,
    'Seller Name': sellers,
    'Brand Name': brands,
    'Sector Name': sectors,
    'Category Name': categories,
    'User ID': user_ids,
    'Transaction Amount': transaction_amounts,
    'Unit Price': unit_prices,
    'Transaction Date': transaction_dates
})


print(df.head())

df.to_csv('data/transaction_data.csv', index=False)
