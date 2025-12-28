import math
from ssi_core.kernel.chronos import L_ALPHA_7

def calculate_proximity(displacement_field_vector, camera_focal_point_vector):
    """
    Calculates the proximity of the 'DisplacementField' to the camera focal point.
    The calculation is weighted by the L_ALPHA_7 constant.
    """
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(displacement_field_vector, camera_focal_point_vector)]))
    weighted_distance = distance * L_ALPHA_7
    return weighted_distance
