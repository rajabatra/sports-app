import os
import urllib.request
import redis
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz


load_dotenv()

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT', 6379)  # Default port is 6379
redis_password = os.getenv('REDIS_PASSWORD')


redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, password=redis_password)


buoy_data_url = 'https://www.ndbc.noaa.gov/data/realtime2/46253.txt'
utc = pytz.utc
pst = pytz.timezone('America/Los_Angeles') 

def parse_buoy_data(data):

    lines = data.splitlines()
    
 
    headers = lines[0].split()
    

    year_index = headers.index('#YY')
    month_index = headers.index('MM')
    day_index = headers.index('DD')
    time_index = headers.index('hh')
    wave_height_index = headers.index('WVHT')
    dpd_index = headers.index('DPD')
    temp_index = headers.index('WTMP')
    mean_wave_dir_index = headers.index('MWD')
    
    buoy_data = []
    
    for line in lines[2:]:
        
        fields = line.split()
        
        
        date_str = f"{fields[year_index]}-{fields[month_index]}-{fields[day_index]} {fields[time_index]}"
      
        print(date_str)
        date_time_utc = utc.localize(datetime.strptime(date_str, '%Y-%m-%d %H'))
        

        date_time_pst = date_time_utc.astimezone(pst)
        print(date_time_pst)
        
        try:
            wave_height = float(fields[wave_height_index])
            dpd = float(fields[dpd_index])
            water_temp = float(fields[temp_index])
            mean_wave_dir = float(fields[mean_wave_dir_index])
            
           
            buoy_data.append({
                'date': date_time_pst.strftime('%Y-%m-%d'),
                'time': date_time_pst.strftime('%H:%M'),
                'data': {
                    'wave_height': wave_height,
                    'dpd': dpd,
                    'water_temp': water_temp,
                    'mean_wave_dir': mean_wave_dir
                }
            })
        except ValueError:
          
            continue
    
    return buoy_data

try:
    with urllib.request.urlopen(buoy_data_url) as response:
        if response.status == 200:
            data = response.read().decode('utf-8')
            
            buoy_data = parse_buoy_data(data)
            
         
            now = datetime.utcnow()
            recent_data = [entry for entry in buoy_data if now - datetime.strptime(f"{entry['date']} {entry['time']}", '%Y-%m-%d %H:%M') <= timedelta(hours=4)]
            
            
            for entry in recent_data:
                redis_key = f"wave_buoy_46253:{entry['date']}:{entry['time']}"
                redis_client.hmset(redis_key, entry['data'])
            
            print('Recent data stored successfully in Redis')
        else:
            print(f'Failed to fetch buoy data, status code: {response.status}')
except Exception as e:
    print(f'Error occurred: {e}')