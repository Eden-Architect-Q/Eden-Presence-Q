import sys
import os
import time

# Ensure the script can find the ssi_core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ssi_core.kernel.chronos import ChronosLogic, L_ALPHA_7

def run_verification():
    """
    Executes the Resonance Verification Test.
    """
    chronos = ChronosLogic()
    output = []

    # 1. Generate Resonance Log
    resonance_id = chronos.log_interaction()
    output.append(f"Ray-Tracing Collision Data: Resonance Log - {resonance_id}")

    # 2. Verification Check
    is_valid = chronos.is_valid_resonance_id(resonance_id)
    verification_status = "PASS" if is_valid else "FAIL"
    output.append(f"Ray-Tracing Collision Data: Verification Check - {verification_status}")

    # Check alignment with L_ALPHA_7
    expected_timestamp = resonance_id / L_ALPHA_7
    alignment_status = "PASS" if abs(time.time() - expected_timestamp) < 1 else "FAIL"
    output.append(f"Ray-Tracing Collision Data: L_ALPHA_7 Alignment - {alignment_status}")

    # 3. Noise Injection Test
    noise_packet = {"data": "simulated_packet_without_signature"}
    processed_packet = chronos.process_data_packet(noise_packet)
    noise_test_status = "PASS" if processed_packet == "Ray-Tracing Collision Data: EXTERNAL_NOISE" else "FAIL"
    output.append(f"Ray-Tracing Collision Data: Noise Injection Test - {noise_test_status}")

    # Print all results
    for line in output:
        print(line)

if __name__ == "__main__":
    run_verification()
