import redis
import os
import threading
import time
from flask import Flask, jsonify, render_template
from buoy_data import get_buoy_data
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

# Create Redis client globally (to be initialized in the app factory)
redis_client = None

# Function to update buoy data periodically
def update_buoy_data_periodically():
    while True:
        data = get_buoy_data()
        if data:
            date, buoy_time, wave_height, dpd, direction, temp, estimated_surf_size = data['date'], data['time'], data['wave_height'], data['dpd'], data['direction'], data['temp'], data['estimated_surf_size']
            key = f"buoy_data:{date}"
            redis_client.hmset(key, {'date': date, 'time': buoy_time, 'wave_height': wave_height, 'dpd': dpd, 'direction': direction, 'temp': temp, 'estimated_surf_size': estimated_surf_size})
            print(f"Buoy data updated at {date} {buoy_time}: {wave_height}m")
        else:
            print("Failed to update buoy data")

        interval = int(os.getenv('UPDATE_INTERVAL', 60))  # Set interval via env variable
        time.sleep(interval)



def create_app():
    app = Flask(__name__)

    metrics = PrometheusMetrics(app)
    
    # metrics
    metrics.info('app_info', 'Application info', version='1.0.0')

    # Redis configuration
    global redis_client
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT', 6379)
    redis_password = os.getenv('REDIS_PASSWORD')
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Start the background thread for periodic updates
    def start_background_thread():
        thread = threading.Thread(target=update_buoy_data_periodically, daemon=True)
        thread.start()

    # Register routes
    @app.route('/update_buoy_data', methods=['POST'])
    def update_buoy_data():
        data = get_buoy_data()
        if not data:
            return jsonify({'error': 'Unable to retrieve buoy data'}), 500

        date, buoy_time, wave_height, dpd, direction, temp, estimated_surf_size = data['date'], data['time'], data['wave_height'], data['dpd'], data['direction'], data['temp'], data['estimated_surf_size']
        key = f"buoy_data:{date}"
        redis_client.hmset(key, {'date': date, 'time': buoy_time, 'wave_height': wave_height, 'dpd': dpd, 'direction': direction, 'temp': temp, 'estimated_surf_size': estimated_surf_size})

        return jsonify({'message': 'Buoy data updated', 'data': data})

    @app.route('/get_buoy_data', methods=['GET'])
    def get_buoy_data_from_redis():
        keys = redis_client.keys("buoy_data:*")
        data = []
        for key in keys:
            data.append(redis_client.hgetall(key))
        return jsonify(data)
    
    @app.route('/')
    def home():
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get the most recent data from Redis
        keys = redis_client.keys("buoy_data:*")
        if keys:
            latest_key = max(keys)  # Assuming keys are in date format like buoy_data:YYYY-MM-DD
            buoy_data = redis_client.hgetall(latest_key)
        else:
            buoy_data = None
        historical_data = []
        for key in keys:
            data = redis_client.hgetall(key)
            data['date'] = key.split(':')[-1]  # Extract date from key
            historical_data.append(data)

        return render_template('index.html', today=today, buoy_data=buoy_data, historical_data=historical_data)

    # Ensure background thread starts when the app is ready
    with app.app_context():
        start_background_thread()

    return app