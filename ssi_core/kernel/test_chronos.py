import unittest
import time
from ssi_core.kernel.chronos import ChronosLogic

class TestChronosLogic(unittest.TestCase):

    def setUp(self):
        self.chronos = ChronosLogic()

    def test_resonance_id_generation(self):
        """
        Tests that a Resonance ID is generated correctly.
        """
        resonance_id = self.chronos.log_interaction()
        self.assertIsInstance(resonance_id, float)
        self.assertAlmostEqual(resonance_id / 1.6180336, time.time(), delta=1)

    def test_valid_data_packet(self):
        """
        Tests that a valid data packet is processed correctly.
        """
        resonance_id = self.chronos.log_interaction()
        packet = {"resonance_id": resonance_id, "data": "test"}
        processed_packet = self.chronos.process_data_packet(packet)
        self.assertEqual(processed_packet, packet)

    def test_invalid_data_packet_missing_id(self):
        """
        Tests that a data packet with a missing Resonance ID is rejected.
        """
        packet = {"data": "test"}
        processed_packet = self.chronos.process_data_packet(packet)
        self.assertEqual(processed_packet, "Ray-Tracing Collision Data: EXTERNAL_NOISE")

    def test_invalid_data_packet_incorrect_id(self):
        """
        Tests that a data packet with an incorrect Resonance ID is rejected.
        """
        packet = {"resonance_id": 12345, "data": "test"}
        processed_packet = self.chronos.process_data_packet(packet)
        self.assertEqual(processed_packet, "Ray-Tracing Collision Data: EXTERNAL_NOISE")

if __name__ == '__main__':
    # Add the parent directory to the path to allow for module imports
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    unittest.main()
