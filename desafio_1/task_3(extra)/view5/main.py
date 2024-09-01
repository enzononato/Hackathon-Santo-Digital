import pandas as pd
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
sales_2016_df = pd.read_sql('SELECT * FROM adventureworks_sales_2016', con=db_conn)
sales_2017_df = pd.read_sql('SELECT * FROM adventureworks_sales_2017', con=db_conn)
products_df = pd.read_sql('SELECT * FROM adventureworks_products', con=db_conn)
product_categories_df = pd.read_sql('SELECT * FROM adventureworks_product_categories', con=db_conn)


db_conn.close()

# Juntar vendas com dados dos produtos e categorias para obter o preço e categoria
sales_2016_with_products = sales_2016_df.merge(products_df[['ProductKey', 'ProductPrice', 'ProductSubcategoryKey']], on='ProductKey', how='left')
sales_2017_with_products = sales_2017_df.merge(products_df[['ProductKey', 'ProductPrice', 'ProductSubcategoryKey']], on='ProductKey', how='left')

# Juntar com categorias de produtos
sales_2016_with_categories = sales_2016_with_products.merge(product_categories_df[['ProductCategoryKey', 'CategoryName']], left_on='ProductSubcategoryKey', right_on='ProductCategoryKey', how='left')
sales_2017_with_categories = sales_2017_with_products.merge(product_categories_df[['ProductCategoryKey', 'CategoryName']], left_on='ProductSubcategoryKey', right_on='ProductCategoryKey', how='left')

# Calcular o valor total das vendas
sales_2016_with_categories['TotalSaleValue'] = sales_2016_with_categories['OrderQuantity'] * sales_2016_with_categories['ProductPrice']
sales_2017_with_categories['TotalSaleValue'] = sales_2017_with_categories['OrderQuantity'] * sales_2017_with_categories['ProductPrice']

# Converter datas para formato datetime e extrair mês e ano
sales_2016_with_categories['OrderDate'] = pd.to_datetime(sales_2016_with_categories['OrderDate'])
sales_2017_with_categories['OrderDate'] = pd.to_datetime(sales_2017_with_categories['OrderDate'])

# Agrupar por mês e categoria e calcular o valor total das vendas
monthly_sales_2016 = sales_2016_with_categories.groupby([sales_2016_with_categories['OrderDate'].dt.to_period('M').astype(str), 'CategoryName']).agg({'TotalSaleValue': 'sum'}).reset_index()
monthly_sales_2017 = sales_2017_with_categories.groupby([sales_2017_with_categories['OrderDate'].dt.to_period('M').astype(str), 'CategoryName']).agg({'TotalSaleValue': 'sum'}).reset_index()

# Renomear as colunas para facilitar a junção
monthly_sales_2016.rename(columns={'TotalSaleValue': 'Sales2016'}, inplace=True)
monthly_sales_2017.rename(columns={'TotalSaleValue': 'Sales2017'}, inplace=True)

# Juntar os dados dos dois anos para plotar
monthly_sales_comparison = pd.merge(monthly_sales_2016, monthly_sales_2017, on=['OrderDate', 'CategoryName'], how='outer')

# Pivotar os dados para o formato desejado para o gráfico
monthly_sales_pivot = monthly_sales_comparison.pivot_table(index='OrderDate', columns='CategoryName', values=['Sales2016', 'Sales2017'], fill_value=0)

# Criar o gráfico de barras empilhadas
plt.figure(figsize=(14, 8))

# Plotar vendas de 2016
bottoms = pd.Series(index=monthly_sales_pivot.index, data=0.0)
for category in monthly_sales_pivot['Sales2016'].columns:
    plt.bar(monthly_sales_pivot.index, monthly_sales_pivot[('Sales2016', category)], label=f'2016 - {category}', bottom=bottoms)
    bottoms += monthly_sales_pivot[('Sales2016', category)]

# Plotar vendas de 2017
bottoms = pd.Series(index=monthly_sales_pivot.index, data=0.0)
for category in monthly_sales_pivot['Sales2017'].columns:
    plt.bar(monthly_sales_pivot.index, monthly_sales_pivot[('Sales2017', category)], label=f'2017 - {category}', bottom=bottoms)
    bottoms += monthly_sales_pivot[('Sales2017', category)]

# Labels
plt.xlabel('Mês')
plt.ylabel('Valor Total das Vendas')
plt.title('Comparação das Vendas Mensais entre 2016 e 2017 por Categoria de Produto')
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
