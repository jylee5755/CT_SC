import requests as req
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import datetime as dt
from tkinter import ttk

def check_valid_date(start_date, end_date):
    count_start = 0
    count_end = 0

    if end_date < start_date:
        raise ValueError("End date must be after start date.")
    
    if len(str(start_date)) != 8 or len(str(end_date)) != 8:
        raise ValueError("Dates must be in YYYYMMDD format.")

def get_weather_data():
    all_items = []
    start_date = start.get()
    start_date_fmt = dt.datetime.strptime(start_date, "%Y%m%d")
    end_date = end.get()
    end_date_fmt = dt.datetime.strptime(end_date, "%Y%m%d")
    region_name = region.get()

    check_valid_date(int(start_date), int(end_date))

    max_req = 100
    num_days = (end_date_fmt - start_date_fmt).days + 1
    total_pages = (num_days + max_req - 1) // max_req
    count_days = 0

    for page in range(1, total_pages + 1):
        count_days += 1

        params = {
            "serviceKey": service_key,
            "numOfRows": str(max_req),
            "pageNo": str(page),
            "dataType": "JSON",
            "dataCd": "ASOS",
            "dateCd": "DAY",
            "startDt": start_date,
            "endDt": end_date,
            "stnIds": str(regiondict[region_name])
        }

        response = req.get(url, params=params, headers={"Content-Type": "application/json"})
        data = response.json()

        try:
            items = data["response"]["body"]["items"]["item"]
            all_items.extend(items)

        except KeyError:
            print(f"{(start_date_fmt + dt.timedelta(days=count_days)).strftime('%Y-%m-%d')} No data available for the selected region and date range.")
            continue

    weather_data = pd.DataFrame(all_items)
    avg_data = weather_data[["tm", "avgTa"]].copy()
    low_data = weather_data[["tm", "minTa"]].copy()
    high_data = weather_data[["tm", "maxTa"]].copy()

    avg_data["avgTa"] = pd.to_numeric(avg_data["avgTa"], errors='coerce')
    low_data["minTa"] = pd.to_numeric(low_data["minTa"], errors='coerce')
    high_data["maxTa"] = pd.to_numeric(high_data["maxTa"], errors='coerce')

    avg_data = avg_data.dropna()
    low_data = low_data.dropna()
    high_data = high_data.dropna()

    plot_weather_data(avg_data, low_data, high_data, start_date_fmt, end_date_fmt, region_name, num_days)

def plot_weather_data(avg_data, low_data, high_data, start_date_fmt, end_date_fmt, region_name, num_days):

    print("기간 중 가장 높은 기온의 날짜 및 값:")
    print(high_data.loc[high_data["maxTa"].idxmax()])
    print("기간 중 가장 낮은 기온의 날짜 및 값:")
    print(low_data.loc[low_data["minTa"].idxmin()])
    plt.figure(num=f"{region_name} - {num_days} days", figsize=(12, 6))

    plt.plot(avg_data["tm"], avg_data["avgTa"], label="Average", color="blue")
    plt.plot(low_data["tm"], low_data["minTa"], label="Minimum", color="green")
    plt.plot(high_data["tm"], high_data["maxTa"], label="Maximum", color="red")

    plt.xlabel("Day")
    plt.ylabel("Temperature (°C)")
    plt.title(f"{region_name} Temperature ({start_date_fmt.strftime('%Y-%m-%d')} ~ {end_date_fmt.strftime('%Y-%m-%d')})")
    plt.xticks(range(0, len(avg_data), 30), rotation=45)
    plt.grid()
    plt.legend()
    plt.show()

global service_key, url, regiondict, root, region, start, end

service_key = "7726d83fb00b5c9384e08d26ec3aa78de8934d72dc67c711235a70cdbfbe60f7"
url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
regiondict = {
    "Seoul" : 108, "Incheon" : 112, "Suwon" : 119, "Cheongju" : 131, 
    "Daejeon" : 133, "Daegu" : 143, "Jeonju" : 146, "Ulsan" : 152, 
    "Changwon" : 155, "Gwangju" : 156, "Busan" : 159, "Jeju" : 184, 
    "Sejong" : 239, "Kimhae" : 253, 
}

root = tk.Tk()
root.title("Weather Data")
root.geometry("600x400")
notice_date = tk.Label(root, text=f"Today's Date: {dt.datetime.now().strftime('%Y-%m-%d')}")
notice_date.grid(row=0, column=0, padx=5, pady=10)

select_region = tk.Label(root, text="Select Region:")
select_region.grid(row=1, column=0, padx=5, pady=10)
region = ttk.Combobox(root, values=list(regiondict.keys()))
region.current(5)
region.grid(row=1, column=1, padx=5, pady=10)

select_start = tk.Label(root, text="Enter Start Date (YYYYMMDD):")
select_start.grid(row=2, column=0, padx=5, pady=10)
start = tk.Entry(root)
start.grid(row=2, column=1, padx=5, pady=10)
start.insert(0, "20250819")

select_end = tk.Label(root, text="Enter End Date (YYYYMMDD):")
select_end.grid(row=3, column=0, padx=5, pady=10)
end = tk.Entry(root)
end.grid(row=3, column=1, padx=5, pady=10)
end.insert(0, "20251119")

btn = tk.Button(root, text = "OK", command=get_weather_data)
btn.grid(row=4, column=1, padx=5, pady=20)

root.mainloop()


