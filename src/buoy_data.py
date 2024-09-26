import requests
from datetime import datetime
import pytz
import numpy as np

# Surf size calculation function
def calculate_surf_size(buoy_wave_size, swell_period, swell_direction):
    # Constants
    beach_orientation = 180  # Huntington Beach facing south
    
    # Convert inputs to float
    buoy_wave_size = float(buoy_wave_size)
    swell_period = float(swell_period)
    swell_direction = float(swell_direction)
    
    # Calculate the swell angle difference
    swell_angle_diff = abs(swell_direction - beach_orientation)
    
    # Impact factor based on the angle difference
    impact_factor = np.cos(np.radians(swell_angle_diff))
    print(impact_factor)
    # Estimate surf size (you can tweak the formula for accuracy)
    estimated_surf_size = 0.5 * buoy_wave_size * (swell_period / 10) * impact_factor * 3.2
    
    if float(estimated_surf_size)<1:
        estimated_surf_size = 1

    return float(estimated_surf_size)

# Function to fetch buoy data
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
        
        # Fetch relevant buoy data
        wave_height = latest_data[8]
        dpd = latest_data[9]  # swell period
        direction = latest_data[11]  # swell direction
        temp = latest_data[14]

        # Calculate estimated surf size
        estimated_surf_size = calculate_surf_size(wave_height, dpd, direction)

        # Prepare the data dictionary
        data = {
            'date': date_obj_pst.strftime('%Y-%m-%d'),
            'time': date_obj_pst.strftime('%H:%M:%S'),
            'wave_height': wave_height,
            'dpd': dpd,
            'direction': direction,
            'temp': temp,
            'estimated_surf_size': round(estimated_surf_size, 2)  
        }
        
        return data
    except Exception as e:
        print(f"Error fetching buoy data: {e}")
        return None

# Example usage
buoy_data = get_buoy_data()
if buoy_data:
    print(buoy_data)