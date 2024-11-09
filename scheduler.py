import schedule
import time
import sqlite3
from datetime import date
from weather_api import get_weather  # Separate weather API function

# Store weather data
def store_weather_data(api_key, cities):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    for city in cities:
        data = get_weather(city, api_key)
        if data:
            cursor.execute('''INSERT INTO weather (city, main, temp, feels_like, dt) VALUES (?, ?, ?, ?, ?)''', 
                           (data['city'], data['main'], data['temp'], data['feels_like'], data['dt']))
    conn.commit()
    conn.close()

def calculate_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    for city in cities:
        today = date.today().strftime('%Y-%m-%d')
        cursor.execute('''SELECT temp, main FROM weather WHERE city = ? AND date(datetime(dt, 'unixepoch')) = ?''', 
                       (city, today))
        results = cursor.fetchall()
        if results:
            temps = [r[0] for r in results]
            conditions = [r[1] for r in results]
            avg_temp = sum(temps) / len(temps)
            max_temp = max(temps)
            min_temp = min(temps)
            dominant_condition = max(set(conditions), key=conditions.count)
            cursor.execute('''INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
                              VALUES (?, ?, ?, ?, ?, ?)''', 
                           (city, today, avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()
    conn.close()

def start_scheduler(api_key, cities):
    schedule.every(5).minutes.do(store_weather_data, api_key, cities)
    schedule.every().day.at("00:00").do(calculate_daily_summary)
    while True:
        schedule.run_pending()
        time.sleep(1)
