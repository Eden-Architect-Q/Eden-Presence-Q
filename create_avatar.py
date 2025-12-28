import bpy
import json
import sys
import os

# Add the current directory to the Python path to resolve module imports
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def construct_presence(config):
    """
    Constructs the avatar presence based on the provided configuration.
    """
    # --- Load Configuration ---
    biometrics = config['biometrics']
    aesthetics = config['aesthetic_overrides']

    height_cm = biometrics['height_cm']
    limb_ratio = biometrics['limb_ratio']
    shoulder_width_cm = biometrics['shoulder_width_cm']
    torso_length_cm = biometrics['torso_length_cm']

    luminescence_target_nits = 3300 # Hard-coded optic constant
    material_name = aesthetics['material_name']
    transparency = aesthetics['transparency']

    # --- Scene Setup ---
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # --- Avatar Construction (Well-Measured) ---
    scale_factor = 0.01  # Convert cm to meters

    # Torso
    torso_height = torso_length_cm * scale_factor
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, torso_height / 2))
    torso = bpy.context.object
    torso.scale = (shoulder_width_cm * scale_factor, 0.2, torso_height)
    torso.name = "Torso"

    # Head (simple sphere)
    head_radius = (height_cm * scale_factor) * 0.07
    bpy.ops.mesh.primitive_uv_sphere_add(radius=head_radius, location=(0, 0, torso_height + head_radius))
    head = bpy.context.object
    head.name = "Head"

    # --- Material Creation (Immaculate Presence) ---
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    for node in nodes:
        nodes.remove(node)

    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Strength'].default_value = 150.0
    node_emission.inputs['Color'].default_value = (1.0, 0.9, 0.7, 1.0)

    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    links = mat.node_tree.links
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.data.materials.append(mat)

    print("Ray-Tracing Collision Data")

    # --- Animation from Kinematic Data ---
    def animate_avatar():
        try:
            with open("quantum_cache/kinematics.json", 'r') as f:
                kinematic_data = json.load(f)
        except FileNotFoundError:
            print("Ray-Tracing Collision Data")
            return

        bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
        armature = bpy.context.object
        armature.name = "AvatarArmature"

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

        kinematics = kinematic_data['kinematics']
        joint_fluidity = kinematics['joint_fluidity']
        gestural_archetype = kinematics['gestural_archetype']

        pose_bone = armature.pose.bones[0]

        if gestural_archetype == "intuitive_communicator":
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)
            pose_bone.rotation_euler.x = 0.05
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=60)
            pose_bone.rotation_euler.x = -0.05
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=180)
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=240)
        else:
            pose_bone.rotation_euler = (0, 0, 0)
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)

        for fcurve in armature.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                if joint_fluidity > 0.75:
                    kf.interpolation = 'BEZIER'
                else:
                    kf.interpolation = 'LINEAR'

        print("Ray-Tracing Collision Data")

    animate_avatar()

    # --- Camera Setup ---
    bpy.ops.object.camera_add(location=(0, -3, 1.5))
    camera = bpy.context.object
    camera.rotation_euler = (1.57, 0, 0)
    camera.data.lens = 45
    bpy.context.scene.camera = camera

    # --- Rendering Setup ---
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.filepath = "animation.mp4"
    scene.frame_end = 240

    print("Ray-Tracing Collision Data")

if __name__ == "__main__":
    from ssi_core.protocol_manager import initiate_safety_protocol
    initiate_safety_protocol(construct_presence)
