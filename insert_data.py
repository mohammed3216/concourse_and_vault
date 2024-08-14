import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
import psycopg2
import os

# Fetching data from the website
url = 'https://screener.in/company/RELIANCE/consolidated/'
webpage = requests.get(url)
soup = bs(webpage.text, 'html.parser')

data = soup.find('section', id="profit-loss", class_="card card-large")
tdata = data.find("table")

table_data = []

for row in tdata.find_all('tr'):
    row_data = []
    for cell in row.find_all(['th', 'td']):
        row_data.append(cell.text.strip())
    table_data.append(row_data)

# Convert table data to DataFrame
df_table = pd.DataFrame(table_data)
df_table.columns = df_table.iloc[0]
df_table = df_table[1:]

# Save DataFrame to CSV (Optional)
df_table.to_csv('table_data.csv', index=False)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    database=os.getenv('POSTGRES_DB', 'concourse'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'password'),
    port=os.getenv('POSTGRES_PORT', '5432')
)

cur = conn.cursor()

# Create table if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS profit_loss (
    year TEXT,
    sales TEXT,
    expenses TEXT,
    operating_profit TEXT,
    opm TEXT,
    other_income TEXT,
    interest TEXT,
    depreciation TEXT,
    profit_before_tax TEXT,
    tax TEXT,
    net_profit TEXT,
    eps TEXT,
    dividend_payout TEXT
);
"""
cur.execute(create_table_query)

# Insert data into PostgreSQL
for index, row in df_table.iterrows():
    insert_query = """
    INSERT INTO profit_loss (year, sales, expenses, operating_profit, opm, 
                             other_income, interest, depreciation, profit_before_tax, 
                             tax, net_profit, eps, dividend_payout)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(insert_query, tuple(row))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data inserted successfully!")
