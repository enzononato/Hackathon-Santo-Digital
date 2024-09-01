import pandas as pd
#from sqlalchemy import create_engine
import mysql.connector

# Função para inserir dados em uma tabela
def inserir_dados(df, tabela, colunas):
    for _, row in df.iterrows():
        valores = [row[col] for col in colunas]
        # Substituir valores NaN antes da inserção
        valores = [val if pd.notna(val) else '' for val in valores]
        cursor.execute(f'''
            INSERT INTO {tabela} ({", ".join(colunas)})
            VALUES ({", ".join(["%s"] * len(colunas))})
        ''', valores)


# Exemplo para ler um arquivo CSV
calendar_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Calendar.csv', encoding='latin1')
customers_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Customers.csv', encoding='latin1')
product_categories_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Product_Categories.csv', encoding='latin1')
product_subcategories_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Product_Subcategories.csv', encoding='latin1')
products_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Products.csv', encoding='latin1')
returns_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Returns.csv', encoding='latin1')
sales_2015_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Sales_2015.csv', encoding='latin1')
sales_2016_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Sales_2016.csv', encoding='latin1')
sales_2017_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Sales_2017.csv', encoding='latin1')
territories_tb = pd.read_csv('desafio_1/dataset/AdventureWorks_Territories.csv', encoding='latin1')

# Configuração da conexão com o banco de dados
db_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="py_adv_works"
)

cursor = db_conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_calendar(
        Date DATE PRIMARY KEY
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_product_categories(
        ProductCategoryKey INT PRIMARY KEY,
        CategoryName VARCHAR(100)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_product_subcategories(
        ProductSubcategoryKey INT PRIMARY KEY,
        SubcategoryName VARCHAR(100),
        ProductCategoryKey INT,
        FOREIGN KEY (ProductCategoryKey) REFERENCES adventureworks_product_categories(ProductCategoryKey)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_products(
        ProductKey INT PRIMARY KEY,
        ProductSubcategoryKey INT,
        ProductSKU VARCHAR(100),
        ProductName VARCHAR(100),
        ModelName VARCHAR(100),
        ProductDescription VARCHAR(100),
        ProductColor VARCHAR(100),
        ProductSize VARCHAR(100),
        ProductStyle VARCHAR(100),
        ProductCost FLOAT,
        ProductPrice FLOAT,
        FOREIGN KEY (ProductSubcategoryKey) REFERENCES adventureworks_product_subcategories(ProductSubcategoryKey)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_customers(
        CustomerKey INT PRIMARY KEY,
        Prefix VARCHAR(100),
        FirstName VARCHAR(100),
        LastName VARCHAR(100),
        BirthDate DATE,
        MaritalStatus VARCHAR(100),
        Gender VARCHAR(100),
        EmailAddress VARCHAR(100),
        AnnualIncome VARCHAR(100),
        TotalChildren INT,
        EducationLevel VARCHAR(100),
        Occupation VARCHAR(100),
        HomeOwner VARCHAR(100)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_territories(
        SalesTerritoryKey INT PRIMARY KEY,
        Region VARCHAR(100),
        Country VARCHAR(100),
        Continent VARCHAR(100)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_sales_2015(
        OrderDate DATE,
        StockDate DATE,
        OrderNumber VARCHAR(100),
        ProductKey INT,
        CustomerKey INT,
        TerritoryKey INT,
        OrderLineItem INT,
        OrderQuantity INT,
        FOREIGN KEY (ProductKey) REFERENCES adventureworks_products(ProductKey),
        FOREIGN KEY (CustomerKey) REFERENCES adventureworks_customers(CustomerKey),
        FOREIGN KEY (TerritoryKey) REFERENCES adventureworks_territories(SalesTerritoryKey)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_sales_2016(
        OrderDate DATE,
        StockDate DATE,
        OrderNumber VARCHAR(100),
        ProductKey INT,
        CustomerKey INT,
        TerritoryKey INT,
        OrderLineItem INT,
        OrderQuantity INT,
        FOREIGN KEY (ProductKey) REFERENCES adventureworks_products(ProductKey),
        FOREIGN KEY (CustomerKey) REFERENCES adventureworks_customers(CustomerKey),
        FOREIGN KEY (TerritoryKey) REFERENCES adventureworks_territories(SalesTerritoryKey)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_sales_2017(
        OrderDate DATE,
        StockDate DATE,
        OrderNumber VARCHAR(100),
        ProductKey INT,
        CustomerKey INT,
        TerritoryKey INT,
        OrderLineItem INT,
        OrderQuantity INT,
        FOREIGN KEY (ProductKey) REFERENCES adventureworks_products(ProductKey),
        FOREIGN KEY (CustomerKey) REFERENCES adventureworks_customers(CustomerKey),
        FOREIGN KEY (TerritoryKey) REFERENCES adventureworks_territories(SalesTerritoryKey)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS adventureworks_returns(
        ReturnDate DATE,
        TerritoryKey INT,
        ProductKey INT,
        ReturnQuantity INT,
        FOREIGN KEY (ProductKey) REFERENCES adventureworks_products(ProductKey),
        FOREIGN KEY (TerritoryKey) REFERENCES adventureworks_territories(SalesTerritoryKey)
    );
''')

tabelas = [
    'adventureworks_calendar',
    'adventureworks_sales_2015',
    'adventureworks_sales_2016',
    'adventureworks_sales_2017',
    'adventureworks_products',
    'adventureworks_customers',
    'adventureworks_territories',
    'adventureworks_product_subcategories',
    'adventureworks_product_categories',
    'adventureworks_returns'
]


# Desabilitar restrições de chave estrangeira
cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')


# Executar TRUNCATE para limpar cada tabela para não incrementar dados repitidos
for tabela in tabelas:
    try:
        cursor.execute(f'TRUNCATE TABLE {tabela};')
        print(f'Tabela {tabela} limpa com sucesso.')
    except mysql.connector.Error as err:
        print(f"Erro ao limpar a tabela {tabela}: {err}")
        
        
# Ajustar formato de datas para a tabela calendar_tb
calendar_tb['Date'] = pd.to_datetime(calendar_tb['Data'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
customers_tb['BirthDate'] = pd.to_datetime(customers_tb['BirthDate'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
returns_tb['ReturnDate'] = pd.to_datetime(returns_tb['ReturnDate'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

# Ajustar formato de datas para as tabelas de vendas
for df in [sales_2015_tb, sales_2016_tb, sales_2017_tb]:
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
    df['StockDate'] = pd.to_datetime(df['StockDate'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')        


# Alterar o tamanho da coluna ProductDescription
cursor.execute('''
    ALTER TABLE adventureworks_products
    MODIFY COLUMN ProductDescription VARCHAR(10000);
''')


#inserir_dados nas tabelas
inserir_dados(calendar_tb, 'adventureworks_calendar', ['Date'])
inserir_dados(sales_2015_tb, 'adventureworks_sales_2015', ['OrderDate', 'StockDate', 'OrderNumber', 'ProductKey', 'CustomerKey', 'TerritoryKey', 'OrderLineItem', 'OrderQuantity'])
inserir_dados(sales_2016_tb, 'adventureworks_sales_2016', ['OrderDate', 'StockDate', 'OrderNumber', 'ProductKey', 'CustomerKey', 'TerritoryKey', 'OrderLineItem', 'OrderQuantity'])
inserir_dados(sales_2017_tb, 'adventureworks_sales_2017', ['OrderDate', 'StockDate', 'OrderNumber', 'ProductKey', 'CustomerKey', 'TerritoryKey', 'OrderLineItem', 'OrderQuantity'])
inserir_dados(products_tb, 'adventureworks_products', ['ProductKey', 'ProductSubcategoryKey', 'ProductSKU', 'ProductName', 'ModelName', 'ProductDescription', 'ProductColor', 'ProductSize', 'ProductStyle', 'ProductCost', 'ProductPrice'])
inserir_dados(customers_tb, 'adventureworks_customers', ['CustomerKey', 'Prefix', 'FirstName', 'LastName', 'BirthDate', 'MaritalStatus', 'Gender', 'EmailAddress', 'AnnualIncome', 'TotalChildren', 'EducationLevel', 'Occupation', 'HomeOwner'])
inserir_dados(territories_tb, 'adventureworks_territories', ['SalesTerritoryKey', 'Region', 'Country', 'Continent'])
inserir_dados(product_subcategories_tb, 'adventureworks_product_subcategories', ['ProductSubcategoryKey', 'SubcategoryName', 'ProductCategoryKey'])
inserir_dados(product_categories_tb, 'adventureworks_product_categories', ['ProductCategoryKey', 'CategoryName'])
inserir_dados(returns_tb, 'adventureworks_returns', ['ReturnDate', 'TerritoryKey', 'ProductKey', 'ReturnQuantity'])

# Commit para salvar as alterações
db_conn.commit()

# Fechar o cursor e a conexão
cursor.close()
db_conn.close()

print("Tabela criada e dados inseridos com sucesso!")