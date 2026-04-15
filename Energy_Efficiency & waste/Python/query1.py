import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.metrics import mean_squared_error

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv('C:/Users/Sahana R/Downloads/enegry.csv')

# =========================
# 2. PREPROCESSING
# =========================

# Convert Timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"], dayfirst=True)

# Extract Month
df["Month"] = df["Timestamp"].dt.month

# Drop Timestamp
df = df.drop(columns=["Timestamp"])

# Encode ONLY Plant (❌ remove MachineID to avoid leakage)
df = pd.get_dummies(df, columns=["Plant"], drop_first=True)

# =========================
# 3. FEATURE ENGINEERING
# =========================

df["Temp_Vibration"] = df["Temperature"] * df["Vibration"]
df["EnergyPerUnit"] = df["EnergyConsumption"] / df["ProductionUnits"]

# =========================
# 4. SPLIT DATA
# =========================

X = df.drop("EnergyConsumption", axis=1)
y = df["EnergyConsumption"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 5. MODELS
# =========================

# Linear Regression
model1 = LinearRegression()
model1.fit(X_train, y_train)

# Random Forest (tuned)
model2 = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=3,
    random_state=42
)
model2.fit(X_train, y_train)

# =========================
# 6. PREDICTIONS
# =========================

pred1 = model1.predict(X_test)
pred2 = model2.predict(X_test)

# =========================
# 7. RMSE CALCULATION
# =========================

rmse1 = np.sqrt(mean_squared_error(y_test, pred1))
rmse2 = np.sqrt(mean_squared_error(y_test, pred2))

print("Linear Regression RMSE:", rmse1)
print("Random Forest RMSE:", rmse2)

# =========================
# 8. GRAPH (MODEL COMPARISON)
# =========================

models = ["Linear Regression", "Random Forest"]
rmse_values = [rmse1, rmse2]

plt.figure(figsize=(6,4))
bars = plt.bar(models, rmse_values)

# Add values on top
for i, v in enumerate(rmse_values):
    plt.text(i, v + 0.5, str(round(v,2)), ha='center')

plt.title("Model Comparison (RMSE)")
plt.ylabel("RMSE")
plt.xlabel("Models")

plt.show()

# =========================
# 9. ACTUAL vs PREDICTED GRAPH
# =========================

plt.scatter(y_test, pred1)
plt.xlabel("Actual Energy")
plt.ylabel("Predicted Energy")
plt.title("Linear Regression: Actual vs Predicted")
plt.show()

# =========================
# 10. ANOMALY DETECTION
# =========================

# Select important features
features = ["Temperature", "Vibration", "Pressure", "EnergyConsumption"]
X_anomaly = df[features]

# Isolation Forest
iso = IsolationForest(contamination=0.01, random_state=42)

iso.fit(X_anomaly)
df["Anomaly"] = iso.predict(X_anomaly)

# Extract anomalies
anomalies = df[df["Anomaly"] == -1]

print("Number of anomalies:", len(anomalies))

# =========================
# 11. ANOMALY VISUALIZATION
# =========================

plt.scatter(df["ProductionUnits"], df["EnergyConsumption"], c=df["Anomaly"])
plt.xlabel("Production Units")
plt.ylabel("Energy Consumption")
plt.title("Anomaly Detection")
plt.show()