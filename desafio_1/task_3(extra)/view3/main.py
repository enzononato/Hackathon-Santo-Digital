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
territories_df = pd.read_sql('SELECT * FROM adventureworks_territories', con=db_conn)
products_df = pd.read_sql('SELECT * FROM adventureworks_products', con=db_conn)
product_subcategories_df = pd.read_sql('SELECT * FROM adventureworks_product_subcategories', con=db_conn)
product_categories_df = pd.read_sql('SELECT * FROM adventureworks_product_categories', con=db_conn)


db_conn.close()

# Concatenar os DataFrames de vendas
sales_df = pd.concat([sales_2015_df, sales_2016_df, sales_2017_df])

# Verificar a estrutura dos DataFrames
print("Estrutura do DataFrame de Produtos:")
print(products_df.head())

# Juntar as tabelas de produtos e subcategorias para obter as categorias
products_with_subcategories = products_df.merge(product_subcategories_df, left_on='ProductSubcategoryKey', right_on='ProductSubcategoryKey', how='left')
products_with_categories = products_with_subcategories.merge(product_categories_df, left_on='ProductCategoryKey', right_on='ProductCategoryKey', how='left')

# Filtrar produtos da categoria 'Bikes'
bikes_df = products_with_categories[products_with_categories['CategoryName'] == 'Bikes']

# Juntar vendas com produtos e regiões
sales_with_products = sales_df.merge(bikes_df[['ProductKey', 'ProductCategoryKey']], on='ProductKey', how='left')
sales_with_territories = sales_with_products.merge(territories_df, left_on='TerritoryKey', right_on='SalesTerritoryKey', how='left')

# Adicionar coluna de ano e mês
sales_with_territories['YearMonth'] = pd.to_datetime(sales_with_territories['OrderDate']).dt.to_period('M').astype(str)

# Agregar vendas totais por região e por mês
heatmap_data = sales_with_territories.groupby(['Region', 'YearMonth']).agg({'OrderQuantity': 'sum'}).reset_index()

# Criar o pivô para o mapa de calor
heatmap_pivot = heatmap_data.pivot(index='Region', columns='YearMonth', values='OrderQuantity')

# mapa de calor
plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_pivot, cmap='YlGnBu', annot=True, fmt='.0f', linewidths=.5)

plt.title('Vendas por Região e por Mês')
plt.xlabel('Mês/Ano')
plt.ylabel('Região')
plt.show()
