import bpy

def _create_halo_object():
    """
    Creates a small icosphere object to be used as a halo particle.
    """
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.01, subdivisions=2)
    halo_obj = bpy.context.object
    halo_obj.name = "HaloParticleObject"
    return halo_obj

def _create_halo_material():
    """
    Creates an emissive, transparent material for the halo object.
    """
    mat = bpy.data.materials.new(name="HaloParticleMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Mix shader for transparency
    node_mix_shader = nodes.new(type='ShaderNodeMixShader')
    node_mix_shader.inputs['Fac'].default_value = 0.8  # Mostly transparent

    # Transparent BSDF
    node_transparent = nodes.new(type='ShaderNodeBsdfTransparent')

    # Emission shader for the halo glow
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Strength'].default_value = 10.0
    node_emission.inputs['Color'].default_value = (1.0, 0.9, 0.7, 1.0)

    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    links = mat.node_tree.links
    links.new(node_transparent.outputs['BSDF'], node_mix_shader.inputs[1])
    links.new(node_emission.outputs['Emission'], node_mix_shader.inputs[2])
    links.new(node_mix_shader.outputs['Shader'], node_output.inputs['Surface'])

    return mat

def setup_atmosphere(humidity_coefficient, scattering_model):
    """
    Initializes a volumetric atmospheric simulation in the scene.
    """
    # --- Volumetric Domain Setup ---
    bpy.ops.mesh.primitive_cube_add(size=20, location=(0, 0, 10))
    domain = bpy.context.object
    domain.name = "AtmosphericDomain"

    # --- Volumetric Material Simulation ---
    mat = bpy.data.materials.new(name="AtmosphericMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    for node in nodes:
        nodes.remove(node)

    node_scatter = nodes.new(type='ShaderNodeVolumeScatter')
    node_scatter.inputs['Density'].default_value = 0.02

    if scattering_model == "rayleigh":
        node_scatter.inputs['Color'].default_value = (0.3, 0.4, 0.8, 1.0)
        node_scatter.inputs['Anisotropy'].default_value = 0.0

    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    links = mat.node_tree.links
    links.new(node_scatter.outputs['Volume'], node_output.inputs['Volume'])

    domain.data.materials.append(mat)

    # --- Particle Physics Simulation ---
    halo_obj = _create_halo_object()
    halo_mat = _create_halo_material()
    halo_obj.data.materials.append(halo_mat)

    # Set the domain as the active object before adding the particle system
    bpy.context.view_layer.objects.active = domain
    bpy.ops.object.particle_system_add()
    particle_system = domain.particle_systems[0]
    settings = particle_system.settings
    settings.name = "AtmosphericParticles"

    settings.count = int(10000 * humidity_coefficient)
    settings.frame_start = 1
    settings.frame_end = 1
    settings.lifetime = 1000
    settings.physics_type = 'NO'

    settings.render_type = 'OBJECT'
    settings.instance_object = halo_obj

    print("Atmospheric Density Fluctuations")
