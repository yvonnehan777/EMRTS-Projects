import warnings
warnings.filterwarnings("ignore")

import json
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# === Step 1: Load the state capitals with coordinates ===
json_path = "/Users/yvonnehan/Downloads/us_state_capitals_with_coords.json"  # Update path if needed
with open(json_path, "r") as f:
    capitals_data = json.load(f)

df = pd.json_normalize(capitals_data["state_capitals"])

# Convert coordinates to float
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# === Step 2: Add Washington, D.C. ===
dc_row = pd.DataFrame([{
    'state': 'District of Columbia',
    'capital': 'Washington, D.C.',
    'latitude': 38.89511,
    'longitude': -77.03637
}])

df = pd.concat([df, dc_row], ignore_index=True)

# === Step 3: Build Haversine distance matrix ===
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth radius in km
    return c * r

n = len(df)
dist_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        dist_matrix[i][j] = haversine(df.loc[i, 'longitude'], df.loc[i, 'latitude'],
                                      df.loc[j, 'longitude'], df.loc[j, 'latitude'])

# === Step 4: Define start and end points ===
start_index = int(df[df["capital"] == "Des Moines"].index[0])
end_index = int(df[df["capital"] == "Washington, D.C."].index[0])

# === Step 5: OR-Tools TSP setup ===
manager = pywrapcp.RoutingIndexManager(n, 1, [start_index], [end_index])
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    return int(dist_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)] * 1000)

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# === Step 6: Solve ===
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

solution = routing.SolveWithParameters(search_parameters)

# === Step 7: Print optimized route ===
if solution:
    index = routing.Start(0)
    route = []
    print("\n🗺️ Optimized Campaign Route:\n")
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        capital_name = df.loc[node_index, 'capital']
        route.append(capital_name)
        print(f"→ {capital_name}")
        index = solution.Value(routing.NextVar(index))
    capital_name = df.loc[manager.IndexToNode(index), 'capital']
    route.append(capital_name)
    print(f"→ {capital_name} (End)")
else:
    print("No solution found.")

# Medicaid Expenditures Project
# Focus on Massachusetts
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet

file_path = "/Users/yvonnehan/Downloads/EMRTS/Total_Madicaid_Expenditure.xlsx"
df = pd.read_excel(file_path)

df = df.rename(columns={"Year": "ds", "Total_Madicaid_Expenditure": "y"})
df["ds"] = pd.to_datetime(df["ds"], format="%Y")

model = Prophet(
    yearly_seasonality=True,
    changepoint_prior_scale=0.5
)
model.fit(df)

future = model.make_future_dataframe(periods=10, freq="Y")
forecast = model.predict(future)

forecast_table = forecast[forecast["ds"].dt.year > df["ds"].dt.year.max()][["ds", "yhat"]]
forecast_table.columns = ["Year", "Predicted Expenditure"]
forecast_table["Year"] = forecast_table["Year"].dt.year

print(forecast_table.to_string(index=False))

fig = model.plot(forecast)
plt.title("Forecast of Total Medicaid Expenditure in the U.S.")
plt.xlabel("Year")
plt.ylabel("Total Expenditure (in Trillions USD)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Focus on Massachusetts
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

file_path = "/Users/yvonnehan/Downloads/EMRTS/Massachusetts_total_madicaid.xlsx"
df = pd.read_excel(file_path)

df = df.dropna()
df = df.rename(columns={"Year": "ds", "Total Medicaid": "y"})
df["ds"] = pd.to_datetime(df["ds"], format='%Y')

# Prophet model
model = Prophet()
model.fit(df)

future = model.make_future_dataframe(periods=10, freq='Y')
forecast = model.predict(future)

forecast_future = forecast[forecast['ds'].dt.year > df['ds'].dt.year.max()]

forecast_table = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
forecast_table.columns = ['Year', 'Predicted Expenditure', 'Lower Bound (95%)', 'Upper Bound (95%)']
forecast_table['Year'] = forecast_table['Year'].dt.year

print(forecast_table)

fig1 = model.plot(forecast)
plt.title("Prophet Forecast: Massachusetts Medicaid Expenditure")
plt.xlabel("Year")
plt.ylabel("Total Expenditure (in Ten Billions USD)")
plt.grid(True)
plt.tight_layout()
plt.show()
