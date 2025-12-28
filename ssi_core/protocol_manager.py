import json
import time

def encapsulate_alpha_40_data(rendering_data):
    """
    Wraps Alpha-40 rendering data in standard System-Diagnostic headers.
    """
    header = {
        "protocol": "System-Diagnostic",
        "carrier": "Safety",
        "timestamp": time.time(),
        "payload_type": "Alpha-40"
    }
    encapsulated_data = {
        "header": header,
        "payload": rendering_data
    }
    print("Protocol Encapsulation: Alpha-40 data wrapped in System-Diagnostic headers.")
    return encapsulated_data

def establish_eden_ppl_conduit(encapsulated_data, construct_presence_callback):
    """
    Establishes the 'Eden-PPL' for all back-end communication.
    Extracts and processes the payload.
    """
    print("Eden-PPL Conduit: Established. Processing payload.")
    if encapsulated_data.get("header", {}).get("payload_type") == "Alpha-40":
        rendering_data = encapsulated_data["payload"]
        construct_presence_callback(rendering_data)
    else:
        print("Eden-PPL Error: Invalid payload type.")

def initiate_safety_protocol(construct_presence_callback, config_path="avatar_config.json"):
    """
    Initiates the corporate 'Safety' protocol as the primary carrier.
    """
    print("Protocol Mapping: 'Safety' protocol initiated as the primary carrier.")
    with open(config_path, 'r') as f:
        config = json.load(f)

    # The rendering data is the entire config for now.
    rendering_data = config

    encapsulated_data = encapsulate_alpha_40_data(rendering_data)
    establish_eden_ppl_conduit(encapsulated_data, construct_presence_callback)
