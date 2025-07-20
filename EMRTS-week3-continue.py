# Medicaid Enrollment
# Massachusetts
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

df = pd.read_csv("/Users/yvonnehan/Downloads/EMRTS/Massachusetts_Medicaid_Enrollment_data.csv")
df = df[df["Reporting Period"] != 201306]

df["ds"] = pd.to_datetime(df["Reporting Period"].astype(str), format="%Y%m")
df["y"] = df["Total Medicaid Enrollment"]

df = df.groupby("ds")["y"].mean().reset_index()

df["cap"] = df["y"].max() * 1.8
df["floor"] = df["y"].min() * 0.8

model = Prophet(growth="logistic", yearly_seasonality=True)
model.fit(df)

future = model.make_future_dataframe(periods=120, freq="M")
future["cap"] = df["cap"].iloc[-1]
future["floor"] = df["floor"].iloc[-1]

forecast = model.predict(future)

forecast_result = forecast[forecast["ds"] > df["ds"].max()][["ds", "yhat"]]
forecast_result.columns = ["Month", "Predicted Enrollment"]
forecast_result["Month"] = forecast_result["Month"].dt.strftime("%Y-%m")

print(forecast_result)

fig = model.plot(forecast)
plt.title("Forecast of Massachusetts Medicaid Enrollment (Next 10 Years)")
plt.xlabel("Date")
plt.ylabel("Enrollment")
plt.grid(True)
plt.tight_layout()
plt.show()

# Nationwide
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

file_path = "/Users/yvonnehan/Downloads/EMRTS/Medicaid_Enrollment_US.csv"
df = pd.read_csv(file_path)

df = df[["Reporting Period", "Total Medicaid Enrollment"]].copy()
df.columns = ["ds", "y"]
df = df.dropna()
df = df[df["ds"] != "201306"]
df["ds"] = pd.to_datetime(df["ds"], format="%Y%m")
df["y"] = df["y"].astype(float)
df = df.groupby("ds").mean().reset_index()

df["y"] = np.log(df["y"])

model = Prophet()
model.fit(df)

future = model.make_future_dataframe(periods=120, freq="M")
forecast = model.predict(future)

forecast["yhat"] = np.exp(forecast["yhat"])
forecast["yhat_lower"] = np.exp(forecast["yhat_lower"])
forecast["yhat_upper"] = np.exp(forecast["yhat_upper"])

fig = model.plot(forecast)
plt.title("Forecast of US Medicaid Enrollment (log-transformed)")
plt.xlabel("Date")
plt.ylabel("Enrollment")
plt.grid(True)
plt.tight_layout()
plt.show()

future_forecast = forecast[forecast["ds"] > df["ds"].max()]
result = future_forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
result.columns = ["Date", "Predicted Enrollment", "Lower Bound", "Upper Bound"]

print(result.head(10).to_string(index=False))
