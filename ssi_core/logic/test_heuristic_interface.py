import unittest
import math
from ssi_core.logic.heuristic_interface import calculate_proximity
from ssi_core.kernel.chronos import L_ALPHA_7

class TestHeuristicInterface(unittest.TestCase):

    def test_calculate_proximity(self):
        """
        Tests the calculate_proximity function with a known vector pair.
        """
        # Based on the values in create_avatar.py
        # manifestation is at (0, 0, 0), camera is at (0, -5, 1.5)
        displacement_field = (0, 0, 0)
        camera_focal_point = (0, -5, 1.5)

        # Manually calculate the expected distance
        expected_distance = math.sqrt((0-0)**2 + (-5-0)**2 + (1.5-0)**2)
        expected_weighted_distance = expected_distance * L_ALPHA_7

        # Calculate the actual distance using the function
        actual_weighted_distance = calculate_proximity(displacement_field, camera_focal_point)

        # Assert that the actual and expected values are close enough to account for floating point inaccuracies
        self.assertAlmostEqual(actual_weighted_distance, expected_weighted_distance, places=7)

if __name__ == '__main__':
    unittest.main()
