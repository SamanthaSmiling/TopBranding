import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Mock data for the Store Table
def generate_store_data(num_stores=1000):
    store_ids = np.random.randint(10000000, 99999999, num_stores)  # 8-digit unique store IDs
    provinces = np.random.choice([f'District {i}' for i in range(1, 36)], num_stores, p=np.random.dirichlet(np.ones(35)))
    cities = np.random.choice([f'City {i}' for i in range(1, 61)], num_stores, p=np.random.dirichlet(np.ones(60)))
    start_dates = [datetime(2019, 1, 1) + timedelta(days=random.randint(0, 1095)) for _ in range(num_stores)]
    owner_ids = np.random.randint(100000000000000000, 999999999999999999, num_stores)
    sales_3_months = np.random.poisson(300000, num_stores)
    levels = np.random.choice(['A', 'B', 'C', 'D', 'E', 'F'], num_stores, p=[0.05, 0.1, 0.15, 0.2, 0.25, 0.25])
    health_scores = np.clip(np.random.normal(80, 10, num_stores), 50, 100)
    financial_products = np.random.choice([True, False], num_stores, p=[0.7, 0.3])
    under_monitoring = np.random.choice([True, False], num_stores, p=[0.05, 0.95])

    store_df = pd.DataFrame({
        'Store ID': store_ids,
        'Province': provinces,
        'City': cities,
        'Start Date': start_dates,
        'Owner ID': owner_ids,
        'Sales (Last 3 Months)': sales_3_months,
        'Store Level': levels,
        'Health Score': health_scores,
        'Financial Products': financial_products,
        'Under Monitoring': under_monitoring
    })

    store_df.to_csv('data/store_data.csv', index=False)
    print("Store Table data generated!")



def generate_product_data(num_products=5000):
    product_ids = np.random.randint(100000000000, 999999999999, num_products)  # 12-digit unique product IDs
    categories = np.random.choice([f'Cata {i}' for i in range(1, 9)], num_products)
    brands = np.random.choice([f'Brand {i}' for i in range(1, 16)], num_products)
    current_stock = np.random.randint(0, 301, num_products)  # Stock between 0-300
    sales_60_days = np.random.poisson(300000, num_products)  # Poisson distribution for 60-day sales
    sales_30_days = np.random.poisson(200000, num_products)  # Poisson distribution for 30-day sales
    stock_progress = np.clip(np.random.normal(0.6, 0.2, num_products), 0, 1)  # 80% between 0.4 and 0.8
    hotspot_stock = np.random.choice([True, False], num_products, p=[0.1, 0.9])  # 10% are hotspot stocks
    stagnant_stock = np.random.choice([True, False], num_products, p=[0.1, 0.9])  # 10% are stagnant stocks
    purchase_price = np.clip(np.random.normal(7000, 1000, num_products), 4000, 10000)  # Purchase price

    # Create DataFrame
    product_df = pd.DataFrame({
        'Product ID': product_ids,
        'Category': categories,
        'Brand': brands,
        'Current Stock': current_stock,
        '60-Day Sales': sales_60_days,
        '30-Day Sales': sales_30_days,
        'Stock Progress (%)': stock_progress,
        'Hotspot Stock': hotspot_stock,
        'Stagnant Stock': stagnant_stock,
        'Purchase Price': purchase_price
    })

    # # Save the DataFrame to the /data/ directory
    # store_df.to_csv('data/store_data.csv', index=False)
    product_df.to_csv('data/product_data.csv', index=False)
    print("Product Table data generated!")


def generate_transaction_data(num_transactions=20000):
    categories = [f'Cata {i}' for i in range(1, 9)]
    probabilities = [0.4, 0.2, 0.15, 0.1, 0.05, 0.04, 0.03, 0.03]
    transaction_ids = np.random.randint(100000000000000000, 999999999999999999, num_transactions)  # 18-digit unique order IDs
    store_ids = np.random.randint(10000000, 99999999, num_transactions)  # Random store IDs
    brands = np.random.choice([f'Brand {i}' for i in range(1, 16)], num_transactions)
    categories = np.random.choice(categories, num_transactions, p=probabilities)
    prices = np.clip(np.random.normal(9000, 1000, num_transactions), 6000, 12000)  # Transaction price
    quantities = np.clip(np.random.normal(5, 2, num_transactions), 1, 10)  # Quantity of products
    amounts = prices * quantities  # Transaction amounts
    used_loans = np.random.choice([True, False], num_transactions, p=[0.7, 0.3])  # 70% use loans
    loans_paid = np.random.choice([True, False], num_transactions, p=[0.8, 0.2])  # 80% loans repaid
    shipment_states = np.random.choice([f'State {i}' for i in range(1, 13)], num_transactions, p=[0.3, 0.3, 0.3] + [0.1 / 9] * 9)  # Shipment status

    # Create DataFrame
    transaction_df = pd.DataFrame({
        'Transaction ID': transaction_ids,
        'Store ID': store_ids,
        'Brand': brands,
        'Category': categories,
        'Price': prices,
        'Quantity': quantities,
        'Amount': amounts,
        'Used Loan': used_loans,
        'Loan Paid': loans_paid,
        'Shipment State': shipment_states
    })

    transaction_df.to_csv('data/transaction_data.csv', index=False)
    print("Transaction Table data generated!")


generate_store_data()
generate_product_data()
generate_transaction_data()
