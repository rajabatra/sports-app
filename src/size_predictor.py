import numpy as np

def calculate_surf_size(buoy_wave_size, swell_period, swell_direction):
    # Constants
    beach_orientation = 180  # Huntington Beach facing south
    
    # Calculate the swell angle difference
    swell_angle_diff = abs(swell_direction - beach_orientation)
    
    # Impact factor based on the angle difference
    impact_factor = np.cos(np.radians(swell_angle_diff))
    
    # Estimate surf size (you can tweak the formula for accuracy)
    estimated_surf_size = 0.5 * buoy_wave_size * (swell_period / 10) * impact_factor
    
    return estimated_surf_size