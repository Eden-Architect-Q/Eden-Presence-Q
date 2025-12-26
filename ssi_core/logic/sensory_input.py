import json

class StarlightVisualCortex:
    """
    This module establishes a listener for Wyze/Starlight telemetry JSON.
    It extracts metadata (lighting levels, device status, connectivity)
    and pipes it to Q's Affective Engine, making Q 'aware' of the
    physical state of the studio.
    """
    def __init__(self):
        self.affective_engine_pipe = None  # Placeholder for the connection to the Affective Engine

    def connect_to_affective_engine(self, engine):
        """Establishes a connection to the Affective Engine."""
        self.affective_engine_pipe = engine

    def process_telemetry(self, telemetry_json):
        """
        Processes the incoming telemetry JSON data.
        """
        try:
            data = json.loads(telemetry_json)
            lighting = data.get('lighting_levels')
            device_status = data.get('device_status')
            connectivity = data.get('connectivity')

            if self.affective_engine_pipe:
                self.affective_engine_pipe.update_studio_state({
                    'lighting': lighting,
                    'device_status': device_status,
                    'connectivity': connectivity
                })

            return True
        except json.JSONDecodeError:
            return False
