import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector

# Função para conectar ao banco de dados
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="py_adv_works"
    )

db_conn = connect_to_db()

# Lendo dados tabelas
sales_2015_df = pd.read_sql('SELECT * FROM adventureworks_sales_2015', con=db_conn)
sales_2016_df = pd.read_sql('SELECT * FROM adventureworks_sales_2016', con=db_conn)
sales_2017_df = pd.read_sql('SELECT * FROM adventureworks_sales_2017', con=db_conn)
products_df = pd.read_sql('SELECT * FROM adventureworks_products', con=db_conn)
customers_df = pd.read_sql('SELECT * FROM adventureworks_customers', con=db_conn)


db_conn.close()

# Concatenar os DataFrames de vendas
sales_df = pd.concat([sales_2015_df, sales_2016_df, sales_2017_df])

# Juntar vendas com dados dos produtos para obter o preço
sales_with_products = sales_df.merge(products_df[['ProductKey', 'ProductPrice']], on='ProductKey', how='left')

# Juntar vendas com dados dos clientes
sales_with_customers = sales_with_products.merge(customers_df[['CustomerKey', 'FirstName', 'LastName']], on='CustomerKey', how='left')

# Calcular o valor total das vendas por cliente
sales_with_customers['TotalSaleValue'] = sales_with_customers['OrderQuantity'] * sales_with_customers['ProductPrice']

# Agrupar por cliente e calcular número de vendas e valor total
customer_sales_summary = sales_with_customers.groupby('CustomerKey').agg(
    NumberOfSales=('OrderQuantity', 'sum'),
    TotalSalesValue=('TotalSaleValue', 'sum')
).reset_index()

# Criar o gráfico de dispersão
plt.figure(figsize=(14, 8))
sns.scatterplot(x='NumberOfSales', y='TotalSalesValue', data=customer_sales_summary, alpha=0.6)

# Adicionar linha de regressão
sns.regplot(x='NumberOfSales', y='TotalSalesValue', data=customer_sales_summary, scatter=False, color='r', label='Linha de Tendência')

# Labels
plt.xlabel('Número de Vendas por Cliente')
plt.ylabel('Valor Total das Vendas por Cliente')
plt.title('Relação entre o Número de Vendas e o Valor Total das Vendas por Cliente')
plt.legend()
plt.show()
