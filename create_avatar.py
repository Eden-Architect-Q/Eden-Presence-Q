import bpy
import json

# --- Load Configuration ---
with open("avatar_config.json", 'r') as f:
    config = json.load(f)

biometrics = config['biometrics']
aesthetics = config['aesthetic_overrides']

height_cm = biometrics['height_cm']
limb_ratio = biometrics['limb_ratio']
shoulder_width_cm = biometrics['shoulder_width_cm']
torso_length_cm = biometrics['torso_length_cm']

luminescence_target_nits = aesthetics['luminescence_target_nits']
material_name = aesthetics['material_name']
transparency = aesthetics['transparency']

# --- Scene Setup ---
# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- Avatar Construction (Well-Measured) ---
# All measurements are in meters for Blender's default scene
scale_factor = 0.01  # Convert cm to meters

# Torso
torso_height = torso_length_cm * scale_factor
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, torso_height / 2))
torso = bpy.context.object
torso.scale = (shoulder_width_cm * scale_factor, 0.2, torso_height)
torso.name = "Torso"

# Head (simple sphere)
head_radius = (height_cm * scale_factor) * 0.07 # Approximate head size
bpy.ops.mesh.primitive_uv_sphere_add(radius=head_radius, location=(0, 0, torso_height + head_radius))
head = bpy.context.object
head.name = "Head"

# --- Material Creation (Immaculate Presence) ---
mat = bpy.data.materials.new(name=material_name)
mat.use_nodes = True
nodes = mat.node_tree.nodes

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Add Emission and Output nodes
node_emission = nodes.new(type='ShaderNodeEmission')
# Approximation of nits to Blender's emission strength. This is non-trivial.
# A strength of ~100 is very bright. Let's use a high value.
node_emission.inputs['Strength'].default_value = 150.0
node_emission.inputs['Color'].default_value = (1.0, 0.9, 0.7, 1.0) # Warm white light

node_output = nodes.new(type='ShaderNodeOutputMaterial')

# Link nodes
links = mat.node_tree.links
links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

# Assign material to all objects
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.data.materials.append(mat)

print("Avatar construction and material application complete.")

# --- Animation from Kinematic Data ---
def animate_avatar():
    try:
        with open("quantum_cache/kinematics.json", 'r') as f:
            kinematic_data = json.load(f)
    except FileNotFoundError:
        print("kinematics.json not found. Skipping animation.")
        return

    # Create a simple armature
    bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    armature = bpy.context.object
    armature.name = "AvatarArmature"

    # A single bone for the torso sway
    bone = armature.data.edit_bones[0]
    bone.head = (0, 0, 0)
    bone.tail = (0, 0, torso_height)

    bpy.ops.object.mode_set(mode='OBJECT')

    # Parent mesh objects to the armature
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.parent = armature
            obj.matrix_parent_inverse = armature.matrix_world.inverted()
            mod = obj.modifiers.new(name='Armature', type='ARMATURE')
            mod.object = armature

    # --- Kinematic-Driven Animation ---
    kinematics = kinematic_data['kinematics']
    joint_fluidity = kinematics['joint_fluidity']
    gestural_archetype = kinematics['gestural_archetype']

    pose_bone = armature.pose.bones[0]

    # Map gestural_archetype to animation type
    if gestural_archetype == "intuitive_communicator":
        # Create a rhythmic, gentle sway with varying speed

        # Frame 1: Neutral position
        pose_bone.rotation_euler = (0, 0, 0)
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)

        # Frame 60: Gentle sway to one side
        pose_bone.rotation_euler.x = 0.05
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=60)

        # Frame 180: Slower sway to the other side
        pose_bone.rotation_euler.x = -0.05
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=180)

        # Frame 240: Return to neutral
        pose_bone.rotation_euler = (0, 0, 0)
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=240)

    else: # Default to a simple, static pose
        pose_bone.rotation_euler = (0, 0, 0)
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)

    # Map joint_fluidity to keyframe interpolation
    # Higher fluidity = smoother (Bezier) interpolation
    for fcurve in armature.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            if joint_fluidity > 0.75:
                kf.interpolation = 'BEZIER'
            else:
                kf.interpolation = 'LINEAR'


    print("Animation data applied.")

animate_avatar()

# --- Camera Setup ---
bpy.ops.object.camera_add(location=(0, -5, 1.5))
camera = bpy.context.object
camera.rotation_euler[0] = 1.3 # Radians, ~75 degrees
bpy.context.scene.camera = camera

# --- Rendering Setup ---
scene = bpy.context.scene
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = "MPEG4"
scene.render.filepath = "animation.mp4"
scene.frame_end = 240

print("Script finished. Ready to render.")
