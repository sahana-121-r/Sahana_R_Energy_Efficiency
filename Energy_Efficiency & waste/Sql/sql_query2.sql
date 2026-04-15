SELECT 
    MachineID,
    Plant,
    Month,
    AVG(EnergyConsumption * 1.0 
        / NULLIF(ProductionUnits,0)) AS AvgEnergyPerUnit,
    CASE 
        WHEN AVG(EnergyConsumption * 1.0 
                 / NULLIF(ProductionUnits,0)) >
             AVG(AVG(EnergyConsumption * 1.0 
                     / NULLIF(ProductionUnits,0)))
             OVER (PARTITION BY Plant, Month)
             + STDEV(AVG(EnergyConsumption * 1.0 
                         / NULLIF(ProductionUnits,0)))
             OVER (PARTITION BY Plant, Month)
        THEN 'Inefficient'
        ELSE 'Efficient'
    END AS EfficiencyFlag
INTO energy_efficiency_flags
FROM [dbo].[Book1]
GROUP BY MachineID, Plant, Month;



