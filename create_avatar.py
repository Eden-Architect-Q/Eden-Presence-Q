import bpy
import json

# --- Load Configuration ---
with open("avatar_config.json", 'r') as f:
    config = json.load(f)

biometrics = config['biometrics']
aesthetics = config['aesthetic_overrides']
visualization_mode = config.get('visualization_mode', 'ETHEREAL')

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

def create_scientific_material(material_name):
    """Creates a material for scientific visualization with SSS and density maps."""
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create Principled BSDF shader for SSS
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = (0, 0)
    node_principled.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1) # Red-ish for organic feel
    node_principled.inputs['Subsurface Weight'].default_value = 0.7 # High SSS
    node_principled.inputs['Subsurface Scale'].default_value = 1.0 # Simulate skin-like scattering
    node_principled.inputs['Roughness'].default_value = 0.5

    # Create procedural noise for density map
    node_noise = nodes.new(type='ShaderNodeTexNoise')
    node_noise.location = (-400, 300)
    node_noise.inputs['Scale'].default_value = 10.0
    node_noise.inputs['Detail'].default_value = 15.0
    node_noise.inputs['Roughness'].default_value = 0.6

    # Create a color ramp to control the density map appearance
    node_color_ramp = nodes.new(type='ShaderNodeValToRGB')
    node_color_ramp.location = (-200, 300)
    node_color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1) # Black
    node_color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1) # White

    # Link noise to color ramp, and color ramp to Principled BSDF roughness/specular
    links = mat.node_tree.links
    links.new(node_noise.outputs['Fac'], node_color_ramp.inputs['Fac'])
    links.new(node_color_ramp.outputs['Color'], node_principled.inputs['Roughness'])
    links.new(node_color_ramp.outputs['Color'], node_principled.inputs['Specular IOR Level'])

    # Create Material Output node
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (200, 0)

    # Link Principled BSDF to output
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

    return mat

# --- Material Creation ---
if visualization_mode == "SCIENTIFIC":
    print("Creating material for Scientific Visualization Mode.")
    mat = create_scientific_material("Forensic-Density-Map")
else: # ETHEREAL mode
    print("Creating material for Ethereal Presence Mode.")
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add Emission and Output nodes
    node_emission = nodes.new(type='ShaderNodeEmission')
    # Approximation of nits to Blender's emission strength.
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
        pose_bone.rotation_euler = (0, 0, 0)
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)
        pose_bone.rotation_euler.x = 0.05
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=60)
        pose_bone.rotation_euler.x = -0.05
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=180)
        pose_bone.rotation_euler = (0, 0, 0)
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=240)
    else: # Default to a simple, static pose
        pose_bone.rotation_euler = (0, 0, 0)
        pose_bone.keyframe_insert(data_path="rotation_euler", frame=1)

    # Map joint_fluidity to keyframe interpolation
    for fcurve in armature.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            if joint_fluidity > 0.75:
                kf.interpolation = 'BEZIER'
            else:
                kf.interpolation = 'LINEAR'

    print("Animation data applied.")

# --- Main Logic ---
if visualization_mode == "SCIENTIFIC":
    print("Scientific Visualization Mode: Exporting to OBJ.")
    # Ensure all objects are selected for export
    bpy.ops.object.select_all(action='SELECT')
    # Export to OBJ
    bpy.ops.wm.obj_export(filepath="structural_analysis_mesh.obj", check_existing=False, forward_axis='Y', up_axis='Z', global_scale=1.0, apply_modifiers=True, export_eval_mode='DAG_EVAL_VIEWPORT', export_selected_objects=True, export_uv=True, export_normals=True, export_materials=False, export_triangulated_mesh=False, export_curves_as_nurbs=False, export_vertex_groups=False, export_object_groups=False, path_mode='AUTO')
    print("Export complete.")

else: # ETHEREAL mode (original functionality)
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
    print("Rendering setup complete. Ready to render animation.")

print("Script finished.")
