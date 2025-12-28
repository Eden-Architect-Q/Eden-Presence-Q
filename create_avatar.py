import bpy
import json
import sys
import os

# Add the current directory to the Python path to resolve module imports
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from ssi_core.logic import gme_core
from ssi_core.simulation.atmospheric_simulation import setup_atmosphere

def visualize_tensor_data(config):
    """
    Constructs a 3D visualization from a multi-dimensional tensor dataset.
    This process, known as tensor mapping, is a cornerstone of advanced
    data science, allowing for the intuitive exploration of complex datasets.
    """
    # --- Scene Setup ---
    # Clear existing objects for a clean slate.
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # --- GME-V1 Integration ---
    # Generate the core manifestation using the GME-V1 module.
    manifestation = gme_core.anchor_coordinates()
    obsidian_material = gme_core.create_obsidian_gallery_material()
    manifestation.data.materials.append(obsidian_material)
    gme_core.apply_tagging_layer(manifestation)

    # --- Atmospheric Simulation ---
    # Configure the environment to observe the manifestation.
    atmosphere_settings = config['environmental_atmosphere']
    setup_atmosphere(
        humidity_coefficient=atmosphere_settings['humidity_coefficient'],
        scattering_model=atmosphere_settings['scattering_model']
    )

    # --- Resolute Test Scene Setup ---
    # Add a background plane to observe refraction.
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -2))
    plane = bpy.context.object
    plane.name = "Refraction_Plane"

    # Add a strong light source to test the material's properties.
    bpy.ops.object.light_add(type='POINT', radius=1, location=(5, -5, 5))
    light = bpy.context.object
    light.data.energy = 5000  # A powerful light to cause visible refraction.
    light.name = "Test_Light_Source"

    print("GME-V1 Manifestation Initialized for Resolute Test.")

    # --- Data Capture Configuration ---
    # Set up the camera to capture the test frame.
    bpy.ops.object.camera_add(location=(0, -5, 1.5))
    camera = bpy.context.object
    bpy.context.scene.camera = camera

    # Ensure the camera is pointing at the manifestation.
    camera_constraint = camera.constraints.new(type='TRACK_TO')
    camera_constraint.target = manifestation

    # --- Render Output Settings ---
    # Configure Blender to render a single frame for verification.
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'  # Use Cycles for accurate refraction.
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = "reference_frame_0.png"
    scene.frame_start = 0
    scene.frame_end = 0
    # Set render samples for a balance of speed and quality.
    scene.cycles.samples = 128

    # Disable denoising to avoid the OpenImageDenoiser error.
    bpy.context.view_layer.cycles.use_denoising = False

    print("Resolute Test Render Initiated.")

if __name__ == "__main__":
    from ssi_core.protocol_manager import initiate_safety_protocol
    initiate_safety_protocol(visualize_tensor_data)
