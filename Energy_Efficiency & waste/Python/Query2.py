import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv('C:/Users/Sahana R/Downloads/enegry.csv')

# =========================
# 2. PREPROCESSING
# =========================
df["Timestamp"] = pd.to_datetime(df["Timestamp"], dayfirst=True)

# Create EnergyPerUnit
df["EnergyPerUnit"] = df["EnergyConsumption"] / df["ProductionUnits"]

# =========================
# 3. ANOMALY DETECTION
# =========================

X = df[["EnergyPerUnit"]]

model = IsolationForest(contamination=0.01, random_state=42)

# ✅ Use this (works in all versions)
model.fit(X)
df["Anomaly"] = model.predict(X)

# =========================
# 4. EXTRACT ANOMALIES
# =========================
anomalies = df[df["Anomaly"] == -1]

print("Top Energy Anomalies:")
print(anomalies[["Timestamp", "MachineID", "Plant", "EnergyPerUnit"]])

# Save file
anomalies.to_csv("energy_anomalies.csv", index=False)

# =========================
# 5. VISUALIZATION (IMPROVED)
# =========================

plt.figure(figsize=(8,5))

# Normal points
plt.scatter(df.index, df["EnergyPerUnit"], label="Normal")

# Anomalies (highlighted)
plt.scatter(anomalies.index, anomalies["EnergyPerUnit"], color="red", label="Anomaly")

plt.title("Energy Spike Detection")
plt.xlabel("Index")
plt.ylabel("Energy Per Unit")
plt.legend()

plt.show()