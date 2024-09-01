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

# Lendo dados tabela
sales_2015_df = pd.read_sql('SELECT * FROM adventureworks_sales_2015', con=db_conn)
sales_2016_df = pd.read_sql('SELECT * FROM adventureworks_sales_2016', con=db_conn)
sales_2017_df = pd.read_sql('SELECT * FROM adventureworks_sales_2017', con=db_conn)
products_df = pd.read_sql('SELECT * FROM adventureworks_products', con=db_conn)
product_subcategories_df = pd.read_sql('SELECT * FROM adventureworks_product_subcategories', con=db_conn)
product_categories_df = pd.read_sql('SELECT * FROM adventureworks_product_categories', con=db_conn)


db_conn.close()

# Concatenar os DataFrames de vendas
sales_df = pd.concat([sales_2015_df, sales_2016_df, sales_2017_df])

# Juntar as tabelas de produtos e subcategorias para obter as categorias
products_with_subcategories = products_df.merge(product_subcategories_df, left_on='ProductSubcategoryKey', right_on='ProductSubcategoryKey', how='left')
products_with_categories = products_with_subcategories.merge(product_categories_df, left_on='ProductCategoryKey', right_on='ProductCategoryKey', how='left')

# Filtrar produtos da categoria 'Bikes'
bikes_df = products_with_categories[products_with_categories['CategoryName'] == 'Bikes']

# Juntar vendas com produtos
sales_with_products = sales_df.merge(bikes_df[['ProductKey', 'ProductName', 'ProductPrice']], on='ProductKey', how='left')

# Calcular lucro por produto
sales_with_products['TotalSaleValue'] = sales_with_products['OrderQuantity'] * sales_with_products['ProductPrice']
product_sales_summary = sales_with_products.groupby('ProductName').agg(
    TotalQuantity=('OrderQuantity', 'sum'),
    TotalSalesValue=('TotalSaleValue', 'sum')
).reset_index()

# Ordenar os produtos por quantidade vendida e pegar os 10 principais
top_10_products = product_sales_summary.sort_values(by='TotalQuantity', ascending=False).head(10)

# Criar o gráfico de barras
plt.figure(figsize=(14, 8))
sns.barplot(x='TotalQuantity', y='ProductName', data=top_10_products, palette='viridis')

# Labels
plt.xlabel('Quantidade Vendida')
plt.ylabel('Produto')
plt.title('Top 10 Produtos Mais Vendidos na Categoria "Bikes"')
plt.show()
