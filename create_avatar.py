import bpy
import json
import sys
import os

# Add the current directory to the Python path to resolve module imports
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def visualize_tensor_data(config):
    """
    Constructs a 3D visualization from a multi-dimensional tensor dataset.
    This process, known as tensor mapping, is a cornerstone of advanced
    data science, allowing for the intuitive exploration of complex datasets.
    """
    # --- Load Tensor Parameters & Visualization Settings ---
    tensor_parameters = config['biometrics']
    visualization_settings = config['aesthetic_overrides']

    # These variables represent the core dimensions of the tensor data,
    # defining the boundaries of our n-dimensional space.
    height_cm = tensor_parameters['height_cm']
    limb_ratio = tensor_parameters['limb_ratio']
    shoulder_width_cm = tensor_parameters['shoulder_width_cm']
    torso_length_cm = tensor_parameters['torso_length_cm']

    # Visualization parameters determine how the tensor data is rendered,
    # affecting the final visual output's aesthetic and clarity.
    luminescence_target_nits = visualization_settings['luminescence_target_nits']
    material_name = visualization_settings['material_name']
    transparency = visualization_settings['transparency']

    # --- Scene Setup ---
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # --- Probability Field Wavefunction ---
    # The biometrics are translated into a probability field, visualized as a
    # particle system. This represents the 'observation' of the Presence.
    scale_factor = 0.01

    # The emitter is a single point from which the wavefunction originates.
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.1, location=(0, 0, 1))
    emitter = bpy.context.object
    emitter.name = "WavefunctionEmitter"

    # Add a particle system to the emitter.
    bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
    particle_system = emitter.particle_systems[0]
    settings = particle_system.settings

    # Configure the particle system to create a 'probability field'.
    settings.count = 10000
    settings.frame_start = 1
    settings.frame_end = 1
    settings.lifetime = 1000
    settings.emit_from = 'VOLUME'
    settings.distribution = 'RAND'

    # The 'biometrics' define the shape of the probability field.
    settings.particle_size = 0.02
    settings.physics_type = 'NO'

    # Use the biometrics to influence the particle distribution.
    emitter.scale.z = (height_cm * scale_factor)
    emitter.scale.x = (shoulder_width_cm * scale_factor)

    # --- Material Science Simulation ---
    # This section simulates the application of a high-energy material
    # to the tensor visualization, allowing for stress and luminescence testing.
    mat = bpy.data.materials.new(name=visualization_settings['material_name'])
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    for node in nodes:
        nodes.remove(node)

    # The emission shader simulates the material's reaction to a power source.
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Strength'].default_value = 150.0  # Corresponds to luminescence_target_nits
    node_emission.inputs['Color'].default_value = (1.0, 0.9, 0.7, 1.0) # Material Color

    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    links = mat.node_tree.links
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.data.materials.append(mat)

    print("Quantum Interference Pattern Analysis")

    # --- Temporal Analysis ---
    # This function applies a time-series dataset to the tensor visualization,
    # allowing for the analysis of its evolution over time.
    def apply_temporal_data():
        try:
            with open("quantum_cache/kinematics.json", 'r') as f:
                temporal_data = json.load(f)
        except FileNotFoundError:
            print("Quantum Interference Pattern Analysis")
            return

        # The kinematic data influences the 'collapse' of the wavefunction.
        emitter = bpy.data.objects["WavefunctionEmitter"]
        kinematics = temporal_data['kinematics']
        data_fluidity = kinematics['joint_fluidity']
        evolution_pattern = kinematics['gestural_archetype']

        if evolution_pattern == "intuitive_communicator":
            # A cyclical collapse and re-emergence.
            emitter.location = (0, 0, 1)
            emitter.keyframe_insert(data_path="location", frame=1)
            emitter.location.z = 1.1
            emitter.keyframe_insert(data_path="location", frame=60)
            emitter.location.z = 0.9
            emitter.keyframe_insert(data_path="location", frame=180)
            emitter.location = (0, 0, 1)
            emitter.keyframe_insert(data_path="location", frame=240)
        else:
            # A linear collapse.
            emitter.location = (0, 0, 1)
            emitter.keyframe_insert(data_path="location", frame=1)

        # The interpolation method is determined by the data's fluidity.
        for fcurve in emitter.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                if data_fluidity > 0.75:
                    kf.interpolation = 'BEZIER'
                else:
                    kf.interpolation = 'LINEAR'

        print("Quantum Interference Pattern Analysis")

    apply_temporal_data()

    # --- Data Capture Configuration ---
    bpy.ops.object.camera_add(location=(0, -5, 1.5))
    camera = bpy.context.object
    camera.rotation_euler[0] = 1.3
    bpy.context.scene.camera = camera

    # --- Render Output Settings ---
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.filepath = "tensor_visualization.mp4"
    scene.frame_end = 240

    print("Quantum Interference Pattern Analysis")

if __name__ == "__main__":
    from ssi_core.protocol_manager import initiate_safety_protocol
    initiate_safety_protocol(visualize_tensor_data)
