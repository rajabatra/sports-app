import os
import redis
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Redis database information from environment variables
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT', 6379)  # Default port is 6379
redis_password = os.getenv('REDIS_PASSWORD')

# Connect to Redis using credentials from the .env file
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, password=redis_password)

def read_buoy_data():
    # Fetch all keys related to wave buoy data
    buoy_keys = redis_client.keys('wave_buoy_46253:*')
    
    if not buoy_keys:
        print("No data found in Redis.")
        return
    
    # Iterate over each key and fetch the stored hash
    for key in buoy_keys:
        # Decode the key from bytes to string
        key_str = key.decode('utf-8')
        
        # Get the hash data for this buoy point
        buoy_data = redis_client.hgetall(key)
        
        # Convert hash data from bytes to string for readability
        buoy_data_readable = {k.decode('utf-8'): v.decode('utf-8') for k, v in buoy_data.items()}
        
        # Print the key and the corresponding data
        print(f"Data for {key_str}:")
        print(buoy_data_readable)
        print()

if __name__ == '__main__':
    read_buoy_data()