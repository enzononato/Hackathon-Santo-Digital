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
