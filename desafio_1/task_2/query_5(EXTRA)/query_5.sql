-- Qual é a receita total gerada por cada cliente em cada trimestre, e qual é a posição de cada cliente em relação à receita total dentro de cada trimestre?

WITH QuarterlyRevenue AS (
    SELECT CustomerKey,
           EXTRACT(QUARTER FROM OrderDate) AS Quarter,
           YEAR(OrderDate) AS Year,
           SUM(OrderQuantity * p.ProductPrice) AS TotalRevenue
    FROM adventureworks_sales_2017 s
    JOIN adventureworks_products p ON s.ProductKey = p.ProductKey
    GROUP BY CustomerKey, Quarter, Year
),
RankedRevenue AS (
    SELECT CustomerKey,
           Quarter,
           Year,
           TotalRevenue,
           RANK() OVER (PARTITION BY Year, Quarter ORDER BY TotalRevenue DESC) AS RevenueRank
    FROM QuarterlyRevenue
)
SELECT c.FirstName, c.LastName, r.Quarter, r.Year, r.TotalRevenue, r.RevenueRank
FROM RankedRevenue r
JOIN adventureworks_customers c ON r.CustomerKey = c.CustomerKey
ORDER BY r.Year, r.Quarter, r.RevenueRank;
