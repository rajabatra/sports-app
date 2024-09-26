import unittest
from buoy_data import calculate_surf_size
import numpy as np

class TestEstimateWaveSize(unittest.TestCase):

    def test_ideal_swell_direction(self):
        """Test wave size estimation for an ideal swell direction (South 180 degrees)"""
        # estimated_surf_size = 0.5 * buoy_wave_size * (swell_period / 10) * impact_factor * 3.2
        wave_height = 2.0  # meters
        dpd = 10  # seconds
        direction = 180  # degrees (true South)
        
        expected_size = 0.5* wave_height * (dpd / 10) * np.cos(np.radians(abs(180-direction)))*3.2
        result = calculate_surf_size(wave_height, dpd, direction)
        
        self.assertEqual(result, expected_size)
    
    def test_non_ideal_swell_direction(self):
        """Test wave size estimation for a non-ideal swell direction"""
        wave_height = 2.0  # meters
        dpd = 10  # seconds
        direction = 150  # degrees (East-Southeast, non-ideal)
        
        expected_size = 0.5* wave_height * (dpd / 10) * np.cos(np.radians(abs(180-direction)))*3.2
        result = calculate_surf_size(wave_height, dpd, direction)
        
        self.assertEqual(result, expected_size)
    
    def test_low_wave_height(self):
        """Test estimation for small waves"""
        wave_height = 0.5  # meters (small wave)
        dpd = 15  # seconds
        direction = 180  # ideal swell direction
        
        expected_size = 0.5* wave_height * (dpd / 10) * np.cos(np.radians(abs(180-direction)))*3.2
        result = calculate_surf_size(wave_height, dpd, direction)
        
        self.assertEqual(result, expected_size)
    
    def test_high_swell_period(self):
        """Test estimation for large swell period"""
        wave_height = 1.0  # meters
        dpd = 20  # seconds (long swell period)
        direction = 180  # ideal swell direction
        
        expected_size = 0.5* wave_height * (dpd / 10) * np.cos(np.radians(abs(180-direction)))*3.2
        result = calculate_surf_size(wave_height, dpd, direction)
        
        self.assertEqual(result, expected_size)
        self.assertGreater(expected_size,3)
    
    def test_poor_angle(self):
        """Test estimation for large swell period"""
        wave_height = 2.0  # meters
        dpd = 9  # seconds (long swell period)
        direction = 260  # nonideal swell direction
        
        expected_size = 0.5* wave_height * (dpd / 10) * np.cos(np.radians(abs(180-direction)))*3.2
        result = calculate_surf_size(wave_height, dpd, direction)
        
        self.assertEqual(result, 1)
        self.assertGreater(expected_size,0.5)

if __name__ == '__main__':
    unittest.main()