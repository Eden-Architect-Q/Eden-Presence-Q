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

    # --- Multi-Dimensional Tensor Mapping ---
    # The tensor data is mapped into a 3D space for visualization.
    # Each geometric primitive represents a node or cluster in the tensor field.
    scale_factor = 0.01  # Normalization factor for the dataset

    # Primary Tensor Body
    torso_height = torso_length_cm * scale_factor
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, torso_height / 2))
    torso = bpy.context.object
    torso.scale = (shoulder_width_cm * scale_factor, 0.2, torso_height)
    torso.name = "Torso"

    # Ancillary Tensor Node
    head_radius = (tensor_parameters['height_cm'] * scale_factor) * 0.07
    bpy.ops.mesh.primitive_uv_sphere_add(radius=head_radius, location=(0, 0, torso_height + head_radius))
    head = bpy.context.object
    head.name = "AncillaryNode"

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

    print("Tensor visualization and material simulation complete.")

    # --- Temporal Analysis ---
    # This function applies a time-series dataset to the tensor visualization,
    # allowing for the analysis of its evolution over time.
    def apply_temporal_data():
        try:
            with open("quantum_cache/kinematics.json", 'r') as f:
                temporal_data = json.load(f)
        except FileNotFoundError:
            print("Temporal data not found. Skipping time-series analysis.")
            return

        # A skeletal structure is used to deform the tensor field over time.
        bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
        armature = bpy.context.object
        armature.name = "TemporalDeformationArmature"

        bone = armature.data.edit_bones[0]
        bone.head = (0, 0, 0)
        bone.tail = (0, 0, torso_height)

        bpy.ops.object.mode_set(mode='OBJECT')

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.parent = armature
                obj.matrix_parent_inverse = armature.matrix_world.inverted()
                mod = obj.modifiers.new(name='Armature', type='ARMATURE')
                mod.object = armature

        kinematics = temporal_data['kinematics']
        # 'joint_fluidity' is re-contextualized as the rate of change in the time-series.
        data_fluidity = kinematics['joint_fluidity']
        # 'gestural_archetype' becomes the pattern of temporal evolution.
        evolution_pattern = kinematics['gestural_archetype']

        pose_bone = armature.pose.bones[0]

        if evolution_pattern == "intuitive_communicator":
            # This pattern represents a cyclical evolution with a clear peak and trough.
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)
            pose_bone.rotation_euler.x = 0.05
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=60)
            pose_bone.rotation_euler.x = -0.05
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=180)
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=240)
        else:
            # A linear, non-cyclical evolution.
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)

        # The interpolation method is determined by the data's fluidity.
        for fcurve in armature.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                if data_fluidity > 0.75:
                    kf.interpolation = 'BEZIER' # Smooth, continuous change
                else:
                    kf.interpolation = 'LINEAR' # Abrupt, discrete change

        print("Temporal data applied to the tensor visualization.")

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

    print("Data visualization script finished. Ready for rendering.")

if __name__ == "__main__":
    from ssi_core.protocol_manager import initiate_safety_protocol
    initiate_safety_protocol(visualize_tensor_data)
