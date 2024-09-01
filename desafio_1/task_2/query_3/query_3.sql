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
