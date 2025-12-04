import requests as req
import pandas as pd
import matplotlib.pyplot as plt


service_key = "7726d83fb00b5c9384e08d26ec3aa78de8934d72dc67c711235a70cdbfbe60f7"
url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"

params = {
    "serviceKey": service_key,
    "numOfRows": "93",
    "pageNo": "1",
    "dataType": "JSON",
    "dataCd": "ASOS",
    "dateCd": "DAY",
    "startDt": "20250819",
    "endDt": "20251119",
    "stnIds": "143"
}

response = req.get(url, params=params, headers={"Content-Type": "application/json"})
data = response.json()

items = data['response']['body']['items']['item']

weather_data = pd.DataFrame(items)
avg_data = weather_data[['tm', 'avgTa']]
low_data = weather_data[['tm', 'minTa']]
high_data = weather_data[['tm', 'maxTa']]

avg_data['avgTa'] = pd.to_numeric(avg_data['avgTa'], errors='coerce')
low_data['minTa'] = pd.to_numeric(low_data['minTa'], errors='coerce')
high_data['maxTa'] = pd.to_numeric(high_data['maxTa'], errors='coerce')

avg_data = avg_data.dropna()
low_data = low_data.dropna()
high_data = high_data.dropna()

print("기간 중 가장 높은 기온의 날짜 및 값:")
print(high_data.loc[high_data['maxTa'].idxmax()])
print("기간 중 가장 낮은 기온의 날짜 및 값:")
print(low_data.loc[low_data['minTa'].idxmin()])

plt.figure(figsize=(12, 6))

plt.plot(avg_data['tm'], avg_data['avgTa'], label='Average', color='blue')
plt.plot(low_data['tm'], low_data['minTa'], label='Minimum', color='green')
plt.plot(high_data['tm'], high_data['maxTa'], label='Maximum', color='red')

plt.xlabel('Day')
plt.ylabel('Temperature (°C)')
plt.title('Daegu Temperature (2025-08-19 ~ 2025-11-19)')
plt.xticks(range(0, len(avg_data), 7), rotation=45)
plt.grid()
plt.legend()
plt.show()