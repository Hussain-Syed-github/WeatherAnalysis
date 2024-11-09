from flask import Flask, render_template, jsonify
import sqlite3
from scheduler import start_scheduler  # Importing scheduler for periodic data retrieval
import threading

app = Flask(__name__)

# Start data retrieval in a background thread
def start_background_thread():
    thread = threading.Thread(target=start_scheduler, args=('your_api_key_here', ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']))
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather_summary/<city>')
def get_weather_summary(city):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT date, avg_temp, max_temp, min_temp, dominant_condition FROM daily_summary WHERE city = ?''', (city,))
    summary = cursor.fetchall()
    conn.close()
    # Format data for JSON response
    data = [{"date": row[0], "avg_temp": row[1], "max_temp": row[2], "min_temp": row[3], "condition": row[4]} for row in summary]
    return jsonify(data)

# Initialize the data retrieval scheduler
start_background_thread()

if __name__ == '__main__':
    app.run(debug=True)
