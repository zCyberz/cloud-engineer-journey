import requests
import json

response = requests.get("https://wttr.in/hanoi?format=j1")
data = response.json()

print("="*30)
print("Weather in Hanoi")
print("="*30)
current = data["current_condition"][0]
print(f"{'Temperature':<15} | {current['temp_C'] +'°C' :<10}")
print(f"{'Humidity':<15} | {current['humidity'] +'%' :<10}")
print(f"{'Wind Speed':<15} | {current['windspeedKmph'] +'km/h' :<10}")
print(f"{'Description':<15} | {current['weatherDesc'][0]['value']:<10}")

with open("weather.json","w") as f:
    json.dump(data,f,indent=4)

print(f"\nSaved to weather.json!")