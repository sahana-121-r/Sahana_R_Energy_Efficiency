SELECT 
    Plant,
    Month,
    SUM(EnergyConsumption) AS TotalEnergy,
    SUM(ProductionUnits) AS TotalUnits,
    SUM(EnergyConsumption)/NULLIF(SUM(ProductionUnits),0) AS EnergyPerUnit
FROM [Book1]
GROUP BY Plant, Month;

SELECT MachineID,
       AVG(EnergyConsumption/NULLIF(ProductionUnits,0)) AS AvgEnergyPerUnit
FROM Book1
GROUP BY MachineID
ORDER BY AvgEnergyPerUnit DESC
OFFSET 0 ROWS
FETCH NEXT 10 ROWS ONLY;