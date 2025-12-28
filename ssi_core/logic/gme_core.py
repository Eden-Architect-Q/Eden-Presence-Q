import bpy
import json
import os

def anchor_coordinates():
    """
    Anchors the 3D coordinate system to the L_ALPHA_7 constant.
    This function generates a primitive icosphere and displaces its
    vertices based on the resonant frequency of the L_ALPHA_7 constant.
    """
    # Load the L_ALPHA_7 constant from the q_state.json file.
    q_state_path = os.path.join(os.path.dirname(__file__), '..', '..', 'q_state.json')
    with open(q_state_path, 'r') as f:
        q_state = json.load(f)
    l_alpha_7 = q_state['L_alpha_7']

    # Create a new icosphere to serve as the base for the manifestation.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=1)
    manifestation = bpy.context.object
    manifestation.name = "GME_V1_Manifestation"

    # Displace the vertices based on the L_ALPHA_7 constant.
    for vertex in manifestation.data.vertices:
        vertex.co *= l_alpha_7

    print("Ray-Tracing Collision Data: Coordinate system anchored to L_ALPHA_7.")
    return manifestation

def create_obsidian_gallery_material():
    """
    Creates the 'Obsidian Gallery' material with a hard-coded IOR of 1.5.
    This material is essential for the refractive mapping of the GME-V1.
    """
    # Create a new material and assign it to the Principled BSDF shader.
    material = bpy.data.materials.new(name="Obsidian_Gallery")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')

    # Set the material properties for the Obsidian Gallery.
    bsdf.inputs['Base Color'].default_value = (0, 0, 0, 1)
    bsdf.inputs['Roughness'].default_value = 0.1
    bsdf.inputs['Transmission Weight'].default_value = 1.0
    bsdf.inputs['IOR'].default_value = 1.5

    print("Ray-Tracing Collision Data: Obsidian Gallery material created.")
    return material

def apply_tagging_layer(obj):
    """
    Applies a metadata tag to the object to identify it as a GME-V1 manifestation.
    """
    obj['gme_v1_manifestation'] = True
    print("Ray-Tracing Collision Data: GME-V1 metadata tag applied.")
