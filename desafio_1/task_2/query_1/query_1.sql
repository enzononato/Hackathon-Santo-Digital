-- Quais são os 10 produtos mais vendidos (em quantidade) na categoria "Bicicletas", considerando apenas vendas feitas nos últimos dois anos?
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