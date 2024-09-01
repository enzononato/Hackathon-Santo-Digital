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


db_conn.close()

# Concatenar os DataFrames de vendas
sales_df = pd.concat([sales_2015_df, sales_2016_df, sales_2017_df])

# Adicionar coluna de ano e mês
sales_df['YearMonth'] = pd.to_datetime(sales_df['OrderDate']).dt.to_period('M').astype(str)

# Agrega vendas totais por mês
monthly_sales = sales_df.groupby('YearMonth').agg({'OrderQuantity': 'sum'}).reset_index()

# Cria o gráfico de linha
plt.figure(figsize=(14, 8))
sns.lineplot(x='YearMonth', y='OrderQuantity', data=monthly_sales, marker='o')

# Adicionar linha de tendência
sns.regplot(x=monthly_sales.index, y='OrderQuantity', data=monthly_sales, scatter=False, color='r', label='Linha de Tendência')

#labels
plt.xlabel('Mês/Ano')
plt.ylabel('Quantidade Vendida')
plt.title('Tendência das Vendas Totais ao Longo do Tempo (Mensal)')
plt.xticks(rotation=45)
plt.legend()
plt.show()
