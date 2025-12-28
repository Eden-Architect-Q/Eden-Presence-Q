import bpy
import json
import os

# Core constant for geometric stability.
L_ALPHA_7 = 1.6180336

def anchor_coordinates(object_name="Anchored_Manifestation"):
    """
    Generates a primitive mesh whose vertex positions are a function of the
    L_ALPHA_7 constant. This prevents geometric drift and ensures all
    manifestations are anchored to the same resonant frequency.
    """
    # Create a simple cube primitive.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1))
    obj = bpy.context.object
    obj.name = object_name

    # Anchor each vertex to the L_ALPHA_7 constant.
    # This is a simple multiplication, but it ensures a deterministic,
    # anchored geometry.
    for vertex in obj.data.vertices:
        vertex.co.x *= L_ALPHA_7
        vertex.co.y *= (L_ALPHA_7 / 2)
        vertex.co.z *= (L_ALPHA_7 * 2)

    return obj

def create_obsidian_gallery_material():
    """
    Defines the 'Obsidian Gallery' material, a core component of the GME.
    It features a hard-coded refractive index of 1.5, ensuring consistent
    light interaction across all manifestations.
    """
    mat = bpy.data.materials.new(name="Obsidian_Gallery")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create a Principled BSDF shader for physically-based rendering.
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = 0, 0
    # Set the refractive index (IOR) to the specified value.
    node_principled.inputs['IOR'].default_value = 1.5
    # Make the material fully transparent for refraction.
    node_principled.inputs['Transmission Weight'].default_value = 1.0
    node_principled.inputs['Base Color'].default_value = (0.8, 0.9, 1.0, 1.0)
    node_principled.inputs['Roughness'].default_value = 0.05 # A slight roughness for realism

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = 400, 0

    # Link the shader to the output.
    links = mat.node_tree.links
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

    return mat

def apply_tagging_layer(obj):
    """
    Attaches identity and emotion variables from the Quantum Cache to the
    generated mesh as non-visual metadata. This 'Tagging Layer' ensures
    that every manifestation carries the signature of its origin.
    """
    # Load identity data from the Quantum Cache (q_state.json).
    try:
        # Construct the path relative to the script's location.
        script_dir = os.path.dirname(os.path.realpath(__file__))
        q_state_path = os.path.join(script_dir, '..', '..', 'q_state.json')
        with open(q_state_path, 'r') as f:
            q_state = json.load(f)
            user_identity = q_state.get("architect", "Unknown")
    except FileNotFoundError:
        user_identity = "Unknown"

    # Hard-code the emotion variable as per the directive.
    emotion_tag = "Resolute"

    # Attach the data as custom properties to the object.
    obj["user_identity"] = user_identity
    obj["emotion_tag"] = emotion_tag
    obj["gme_version"] = "GME-V1"

    print(f"Tagging Layer Applied: User='{user_identity}', Emotion='{emotion_tag}'")
