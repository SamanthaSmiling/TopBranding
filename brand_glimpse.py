import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime 
import plotly.graph_objects as go
import textwrap

def read_file(filename):
    df = pd.read_csv(filename)
    return df

def glimpse(df):
    # time to datetime 
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

    # Year and Month
    df['Year'] = df['Transaction Date'].dt.year
    df['Month'] = df['Transaction Date'].dt.month

    # ---- Brand's health checking ---- #

    # 1. 各品牌分年累计成交直方图
    brand_sales_by_year = df.groupby(['Brand Name', 'Year'])['Transaction Amount'].sum().unstack()

    # 2. 成交金额最高的品牌
    top_brand = df.groupby('Brand Name')['Transaction Amount'].sum().idxmax()

    # 成交最高品牌每个月的成交走势图，计算YOY同比
    top_brand_sales_by_month = df[df['Brand Name'] == top_brand].groupby(['Year', 'Month'])['Transaction Amount'].sum().unstack()
    top_brand_yoy = top_brand_sales_by_month.pct_change(periods=12, axis=1)  # 计算同比变化

    # 3. 成交最高品牌在各一级类目和二级类目的环形占比图
    top_brand_sector_category_distribution = df[df['Brand Name'] == top_brand].groupby(['Sector Name', 'Category Name'])['Transaction Amount'].sum()

    # 4. 成交最高品牌在不同商家的销量直方图，按销量降序排序
    top_brand_seller_distribution = df[df['Brand Name'] == top_brand].groupby('Seller Name')['Transaction Amount'].sum().sort_values(ascending=False)

    # 5. 全部成交流向一级类目和二级类目的桑基图数据
    sector_category_flow = df.groupby(['Sector Name', 'Category Name'])['Transaction Amount'].sum().reset_index()


    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # ---- 图表1: 各品牌分年累计成交---- #
    brand_sales_by_year.plot(kind='bar', stacked=True, ax=axes[0, 0], colormap='tab20')
    axes[0, 0].set_title('Cumulative Sales by Brand per Year')
    axes[0, 0].set_xlabel('Brand Name')
    axes[0, 0].set_ylabel('Sales')

    # ---- 图表2: 成交最高品牌每个月的成交走势图，YOY同比 ---- #
    top_brand_sales_by_month.T.plot(ax=axes[0, 1], marker='o')
    axes[0, 1].set_title(f'Monthly Sales Trend for Top Brand: {top_brand}')
    axes[0, 1].set_xlabel('Month')
    axes[0, 1].set_ylabel('Sales')

    # YOY同比变化
    ax2_twin = axes[0, 1].twinx()
    top_brand_yoy.T.plot(ax=ax2_twin, color='r', linestyle='--', legend=False)
    ax2_twin.set_ylabel('YOY (%)')

    # ---- 图表3: 成交最高品牌在各一级类目和二级类目的双层环形占比图 ---- #

    def autopct_filter(pct, values, threshold):
        absolute = int(np.round(pct / 100. * np.sum(values)))
        # 只有当数值大于阈值时才显示百分比
        return f'{pct:.1f}%' if absolute > threshold else ''

    # 计算成交最高品牌的一级类目和二级类目成交总金额
    top_brand_sector_distribution = df[df['Brand Name'] == top_brand].groupby('Sector Name')['Transaction Amount'].sum()
    top_brand_category_distribution = df[df['Brand Name'] == top_brand].groupby('Category Name')['Transaction Amount'].sum()

    sector_category_mapping = df[df['Brand Name'] == top_brand].groupby(['Sector Name', 'Category Name'])['Transaction Amount'].sum().reset_index()

    # 内外环数据
    sector_amounts = top_brand_sector_distribution.values  # 一级类目的成交金额
    category_amounts = sector_category_mapping['Transaction Amount'].values  # 二级类目的成交金额

    # 类目标签
    sector_labels = top_brand_sector_distribution.index
    category_labels = sector_category_mapping['Category Name']

    # 双层环形图
    fig, ax = plt.subplots()

    # 内环：一级类目
    ax.pie(sector_amounts, labels=sector_labels, radius=1, 
        autopct=lambda pct: autopct_filter(pct, sector_amounts, 5),  # 只显示大于 10000 的百分比
        startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'), 
        colors=plt.cm.Set3(np.linspace(0, 1, len(sector_labels))))

    # 外环：二级类目
    ax.pie(category_amounts, labels=None, radius=1.3, 
        autopct=lambda pct: autopct_filter(pct, category_amounts, 500000),  # 只显示大于 5000 的百分比
        startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'), 
        colors=plt.cm.Pastel1(np.linspace(0, 1, len(category_labels))))

    ax.set(aspect="equal", title=f'Sector & Category Distribution for Top Brand: {top_brand}')


    # ---- 图表4: 成交最高品牌在不同商家的销量，按销量降序 ---- #
    top_brand_seller_distribution.plot(kind='bar', ax=axes[1, 1], color='steelblue')
    axes[1, 1].set_title(f'Sales by Seller for Top Brand: {top_brand}')
    axes[1, 1].set_xlabel('Seller Name')
    axes[1, 1].set_ylabel('Sales')
    axes[1, 1].tick_params(axis='x', rotation=90)

    conclusion_text = "For illustration purposes"
    wrapped_text = "\n".join(textwrap.wrap(conclusion_text, width=80))
    fig.text(0.5, 0.9, wrapped_text, ha='center', fontsize=12)
    # Adjust layout to ensure the text fits well
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


    plt.tight_layout()
    plt.show()

    # ---- 全部成交流向一级类目和二级类目 ---- #

    sources = sector_category_flow['Sector Name']
    targets = sector_category_flow['Category Name']
    values = sector_category_flow['Transaction Amount']

    # 将sector和category映射到索引
    labels = list(sources.unique()) + list(targets.unique())
    source_indices = [labels.index(source) for source in sources]
    target_indices = [labels.index(target) for target in targets]

    # 桑基图
    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
        )
    ))


    fig_sankey.show()


filename = "data/transaction_data.csv"
df = read_file(filename)
glimpse(df)