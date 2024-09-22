import requests
from datetime import datetime
import pytz

def get_buoy_data():
    try:
        url = 'https://www.ndbc.noaa.gov/data/realtime2/46253.txt'
        response = requests.get(url)
        response.raise_for_status()

        
        lines = response.text.splitlines()
        latest_data = lines[2].split()  
        
        # Extract the date and time information from the columns
        year = latest_data[0]
        month = latest_data[1]
        day = latest_data[2]
        hour = latest_data[3]
        minute = latest_data[4]
        
        # Combine date and time to a single string in UTC
        date_str = f"{year}-{month}-{day} {hour}:{minute}"
        date_obj_utc = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        
        # Set UTC as the timezone for the date_obj_utc
        utc_zone = pytz.utc
        date_obj_utc = utc_zone.localize(date_obj_utc)
        pst_zone = pytz.timezone('America/Los_Angeles')
        date_obj_pst = date_obj_utc.astimezone(pst_zone)
        
  
        wave_height = latest_data[8]
        dpd = latest_data[9]
        direction = latest_data[11]
        temp = latest_data[14]


        data = {
            'date': date_obj_pst.strftime('%Y-%m-%d'),
            'time': date_obj_pst.strftime('%H:%M:%S'),
            'wave_height': wave_height,
            'dpd':dpd,
            'direction': direction,
            'temp':temp
        }
        
        return data
    except Exception as e:
        print(f"Error fetching buoy data: {e}")
        return None