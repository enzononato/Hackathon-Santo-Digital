# AdventureWorks Analysis

Este repositório contém uma análise detalhada do banco de dados AdventureWorks, incluindo a criação de um Diagrama Entidade-Relacionamento (DER) e a elaboração de queries SQL para responder a perguntas específicas de negócios.

## Estrutura do Projeto

- **Diagrama Entidade-Relacionamento (DER):** O DER foi criado utilizando o Lucidchart e reflete a estrutura das tabelas fornecidas no banco de dados AdventureWorks.
- **Base de Dados SQL:** A partir do DER e dos arquivos CSV fornecidos, uma base de dados foi criada para possibilitar a análise.
- **Queries SQL:** As consultas SQL foram elaboradas para responder a perguntas de negócios específicas, detalhadas a seguir.

## Requisitos

- MySQL Workbench
- Instalar as bibliotecas dentro do arquivo requirements.txt para execução da tarefa 1 e a tarefa extra. O comando que deve ser utilizado é "pip install -r requirements.txt"

## Configuração

### Download do Dataset:

Faça o download ou importe o dataset AdventureWorks para seu ambiente SQL.

### Criação da Base de Dados:

- Utilize o DER fornecido para criar as tabelas no seu ambiente SQL.
- Importe os dados dos arquivos CSV para as respectivas tabelas.

## Diagrama Entidade-Relacionamento (DER)

O DER foi criado utilizando o Lucidchart e descreve a estrutura das tabelas do banco de dados AdventureWorks. O diagrama reflete as relações entre as tabelas principais, como vendas, clientes, produtos e territórios.

## Queries SQL

### 1. Produtos mais vendidos na categoria "Bicicletas"

**Pergunta:** Quais são os 10 produtos mais vendidos (em quantidade) na categoria "Bicicletas", considerando apenas vendas feitas nos últimos dois anos?

**Query:**

```sql
SELECT ProductName, SUM(TotalQuantity) AS TotalQuantity
FROM (
    -- Vendas em 2016
    SELECT p.ProductName,
           SUM(s.OrderQuantity) AS TotalQuantity
    FROM adventureworks_sales_2016 s
    JOIN adventureworks_products p ON s.ProductKey = p.ProductKey
    JOIN adventureworks_product_subcategories ps ON p.ProductSubcategoryKey = ps.ProductSubcategoryKey
    JOIN adventureworks_product_categories c ON ps.ProductCategoryKey = c.ProductCategoryKey
    WHERE c.CategoryName = 'Bikes'
    GROUP BY p.ProductName

    UNION ALL

    -- Vendas em 2017
    SELECT p.ProductName,
           SUM(s.OrderQuantity) AS TotalQuantity
    FROM adventureworks_sales_2017 s
    JOIN adventureworks_products p ON s.ProductKey = p.ProductKey
    JOIN adventureworks_product_subcategories ps ON p.ProductSubcategoryKey = ps.ProductSubcategoryKey
    JOIN adventureworks_product_categories c ON ps.ProductCategoryKey = c.ProductCategoryKey
    WHERE c.CategoryName = 'Bikes'
    GROUP BY p.ProductName
) AS CombinedSales

-- Agrupar e ordenar os resultados combinados
GROUP BY ProductName
ORDER BY TotalQuantity DESC
LIMIT 10
```

### 2. Cliente com maior número de pedidos em todos os trimestres do último ano fiscal

**Pergunta:** Qual é o cliente que tem o maior número de pedidos realizados, considerando apenas clientes que fizeram pelo menos um pedido em cada trimestre do último ano fiscal?

**Query**

```sql
WITH QuarterlyOrders AS (
    SELECT CustomerKey,
           EXTRACT(QUARTER FROM OrderDate) AS Quarter
    FROM adventureworks_sales_2017
    GROUP BY CustomerKey, Quarter
),
CustomersWithMinimumQuarters AS (
    SELECT CustomerKey
    FROM QuarterlyOrders
    GROUP BY CustomerKey
    HAVING COUNT(DISTINCT Quarter) >= 1  -- Ajuste para pelo menos 1 trimestre
),
TotalOrders AS (
    SELECT CustomerKey,
           COUNT(DISTINCT OrderNumber) AS TotalOrders
    FROM adventureworks_sales_2017
    WHERE CustomerKey IN (SELECT CustomerKey FROM CustomersWithMinimumQuarters)
    GROUP BY CustomerKey
)
SELECT c.FirstName, c.LastName, t.TotalOrders
FROM TotalOrders t
JOIN adventureworks_customers c ON t.CustomerKey = c.CustomerKey
ORDER BY t.TotalOrders DESC
LIMIT 1;

```

### 3. Mês com maior valor de vendas e receita média superior a 500

**Pergunta:** Em qual mês do ano ocorrem mais vendas (em valor total), considerando apenas os meses em que a receita média por venda foi superior a 500 unidades monetárias?

**Query**

```sql
WITH MonthlySales AS (
    SELECT 
        EXTRACT(MONTH FROM s.OrderDate) AS Month,
        EXTRACT(YEAR FROM s.OrderDate) AS Year,
        SUM(s.OrderQuantity * p.ProductPrice) AS TotalRevenue,
        AVG(s.OrderQuantity * p.ProductPrice) AS AverageRevenuePerSale
    FROM (
        SELECT * FROM adventureworks_sales_2015
        UNION ALL
        SELECT * FROM adventureworks_sales_2016
        UNION ALL
        SELECT * FROM adventureworks_sales_2017
    ) s
    JOIN adventureworks_products p ON s.ProductKey = p.ProductKey
    GROUP BY Month, Year
)
SELECT Month, Year, TotalRevenue, AverageRevenuePerSale
FROM MonthlySales
WHERE AverageRevenuePerSale > 500
ORDER BY TotalRevenue DESC
LIMIT 1;

```


### 4. Vendedores com vendas acima da média e crescimento superior a 10%


**Pergunta:** Quais vendedores tiveram vendas com valor acima da média no último ano fiscal e também tiveram um crescimento de vendas superior a 10% em relação ao ano anterior?

**Query**

```sql
WITH SalesByYear AS (
    SELECT
        EXTRACT(YEAR FROM s.OrderDate) AS Year,
        t.SalesTerritoryKey,
        SUM(s.OrderQuantity * p.ProductPrice) AS TotalRevenue
    FROM (
        SELECT * FROM adventureworks_sales_2015
        UNION ALL
        SELECT * FROM adventureworks_sales_2016
        UNION ALL
        SELECT * FROM adventureworks_sales_2017
    ) s
    JOIN adventureworks_products p ON s.ProductKey = p.ProductKey
    JOIN adventureworks_territories t ON s.TerritoryKey = t.SalesTerritoryKey
    GROUP BY Year, t.SalesTerritoryKey
),
GrowthCalculation AS (
    SELECT
        CurrentYear.SalesTerritoryKey,
        CurrentYear.Year AS CurrentYear,
        PreviousYear.Year AS PreviousYear,
        CurrentYear.TotalRevenue AS CurrentRevenue,
        PreviousYear.TotalRevenue AS PreviousRevenue,
        (CurrentYear.TotalRevenue - PreviousYear.TotalRevenue) / PreviousYear.TotalRevenue * 100 AS GrowthPercentage
    FROM SalesByYear CurrentYear
    JOIN SalesByYear PreviousYear
    ON CurrentYear.SalesTerritoryKey = PreviousYear.SalesTerritoryKey
    AND CurrentYear.Year = PreviousYear.Year + 1
),
AboveAverage AS (
    SELECT 
        SalesTerritoryKey, 
        CurrentYear, 
        CurrentRevenue, 
        GrowthPercentage
    FROM GrowthCalculation
    WHERE GrowthPercentage > 10  -- Filtro de crescimento acima de 10%
)
SELECT * FROM AboveAverage
WHERE CurrentRevenue > (
    SELECT AVG(CurrentRevenue)
    FROM GrowthCalculation
    WHERE CurrentYear = (SELECT MAX(CurrentYear) FROM GrowthCalculation)
);
```

--- 

### 5. Visualizações de Dados - AdventureWorks

Este conjunto de visualizações foi criado para fornecer insights sobre o desempenho da empresa AdventureWorks usando o conjunto de dados disponível.

## Visualização #1: Gráfico de Linha - Tendência das Vendas Totais ao Longo do Tempo

**Descrição:**
- **Objetivo:** Mostrar a tendência das vendas mensais ao longo do tempo e identificar os meses de pico de vendas.
- **Eixos:**
  - **Eixo X:** Meses (ordenados cronologicamente)
  - **Eixo Y:** Total de Vendas (em valor monetário)
- **Elementos:**
  - Linha principal conectando os valores mensais de vendas.
  - Destaque visual nos meses de pico de vendas.
  - Linha de tendência para prever vendas futuras com base nos dados históricos.
- **Insights Esperados:** Identificação de padrões sazonais, meses de alta e baixa nas vendas, e projeções de vendas futuras.

## Visualização #2: Gráfico de Barras - Top 10 Produtos Mais Vendidos na Categoria "Bicicletas"

**Descrição:**
- **Objetivo:** Apresentar os 10 produtos mais vendidos na categoria "Bicicletas" e o lucro gerado por cada produto.
- **Eixos:**
  - **Eixo X:** Produtos (os 10 mais vendidos)
  - **Eixo Y:** Quantidade Vendida (barra principal) e Lucro Gerado (barra secundária ou sobreposta)
- **Elementos:**
  - Barras representando a quantidade vendida de cada produto.
  - Barras secundárias ou sobrepostas para mostrar o lucro gerado por produto.
- **Insights Esperados:** Identificação dos produtos mais lucrativos dentro da categoria de "Bicicletas" e relação entre quantidade vendida e lucro.

## Visualização #3: Mapa de Calor - Vendas por Região e Mês

**Descrição:**
- **Objetivo:** Visualizar o volume total de vendas por região e mês, permitindo análise de desempenho regional e sazonal.
- **Eixos:**
  - **Eixo X:** Meses
  - **Eixo Y:** Regiões
- **Elementos:**
  - Cores representando a intensidade do volume de vendas (quanto mais intenso, maior o volume).
  - Filtro interativo para permitir a seleção de diferentes categorias de produtos.
- **Insights Esperados:** Compreensão de quais regiões são mais fortes em termos de vendas e em quais meses, além de como essas dinâmicas variam por categoria de produto.

## Visualização #4: Gráfico de Dispersão - Relação entre Número de Vendas e Valor Total por Cliente

**Descrição:**
- **Objetivo:** Explorar a relação entre o número de vendas e o valor total de vendas por cliente.
- **Eixos:**
  - **Eixo X:** Número de Vendas (por cliente)
  - **Eixo Y:** Valor Total das Vendas (por cliente)
- **Elementos:**
  - Pontos dispersos representando cada cliente.
  - Linha de regressão para destacar a tendência geral.
- **Insights Esperados:** Identificação de padrões de compra entre os clientes, incluindo possíveis outliers e a correlação entre frequência de compra e valor total.

## Visualização #5: Gráfico de Barras Empilhadas - Comparação de Vendas Mensais entre Dois Anos

**Descrição:**
- **Objetivo:** Comparar as vendas mensais de dois anos consecutivos e analisar as tendências de crescimento ou declínio por categoria de produto.
- **Eixos:**
  - **Eixo X:** Meses
  - **Eixo Y:** Vendas Totais (em valor monetário)
- **Elementos:**
  - Barras empilhadas para representar as vendas de cada categoria de produto.
  - Comparação direta entre as barras de cada ano para cada mês.
- **Insights Esperados:** Identificação de mudanças no desempenho mensal e crescimento ou declínio de categorias específicas de produtos ao longo dos anos.

## Screenshots

### Visualização 1

![Visualização 1](https://cdn.discordapp.com/attachments/801955167208734760/1279892529071784106/view1.png?ex=66d6184e&is=66d4c6ce&hm=0655f21644b151e7588ce462be3b03688d399feaa50115452be33e22d9573e0b&)


### Visualização 2

![Visualização 2](https://cdn.discordapp.com/attachments/801955167208734760/1279891831718416475/view_2.png?ex=66d617a7&is=66d4c627&hm=e5c2dbe973eb8ff18d3c64bea812cf8612a2990048983a343765ecf4ed5fb452&)



### Visualização 3

![Visualização 3](https://cdn.discordapp.com/attachments/801955167208734760/1279891867340898336/view_3.png?ex=66d617b0&is=66d4c630&hm=07658dfbb11ef8bd5359d1633028403605ff13e165cf7df565c5ddff6756323b&)


### Visualização 4

![Visualização 4](https://media.discordapp.net/attachments/801955167208734760/1279894043622641734/view_4.png?ex=66d619b7&is=66d4c837&hm=8df7c269308c8a3f0ca0254cc9769ed12f125dab8848c942b189eef9b043fad3&=&format=webp&quality=lossless&width=965&height=498)


### Visualização 5

![Visualização 5](https://cdn.discordapp.com/attachments/801955167208734760/1279895370213884057/view_5.png?ex=66d61af3&is=66d4c973&hm=5d2bef5a2e21fe8be181f7794cf88a6b6c6e6faa398cc7d556345edd80d1a848&)
