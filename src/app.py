from flask import Flask, jsonify
import redis
import os
from buoy_data import get_buoy_data

app = Flask(__name__)

# Configure Redis connection
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD')

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Route to fetch and store the most recent buoy data
@app.route('/update_buoy_data', methods=['POST'])
def update_buoy_data():
    data = get_buoy_data()
    if not data:
        return jsonify({'error': 'Unable to retrieve buoy data'}), 500

    date, time, wave_height, dpd, direction, temp = data['date'], data['time'], data['wave_height'], data['dpd'], data['direction'], data['temp']
    key = f"buoy_data:{date}"
    
    # Update data if the same date exists or add a new entry
    redis_client.hmset(key, {'date': date, 'time': time, 'wave_height': wave_height, 'dpd': dpd, 'ditrection': direction, 'temp': temp})
    
    return jsonify({'message': 'Buoy data updated', 'data': data})

# Route to view buoy data from Redis
@app.route('/get_buoy_data', methods=['GET'])
def get_buoy_data_from_redis():
    keys = redis_client.keys("buoy_data:*")
    data = []
    for key in keys:
        data.append(redis_client.hgetall(key))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)