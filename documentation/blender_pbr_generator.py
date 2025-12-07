import bpy

def hex_to_rgb(hex_color):
    """Converts a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1,)

def create_polished_gold():
    """Creates a Polished Gold PBR material."""
    mat = bpy.data.materials.new(name="Gold_Polished")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    # Set material properties based on documentation
    bsdf.inputs["Base Color"].default_value = hex_to_rgb("#D4A574")
    bsdf.inputs["Roughness"].default_value = 0.35
    bsdf.inputs["Metallic"].default_value = 1.0

    # Add subtle surface imperfections with a noise texture
    noise_texture = nodes.new(type="ShaderNodeTexNoise")
    noise_texture.inputs["Scale"].default_value = 50.0
    noise_texture.location = (-300, 0)

    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.inputs["Strength"].default_value = 0.1
    bump_node.location = (-150, 0)

    mat.node_tree.links.new(noise_texture.outputs["Fac"], bump_node.inputs["Height"])
    mat.node_tree.links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])
    
    print("Created 'Gold_Polished' material.")

def create_clear_diamond():
    """Creates a Clear Diamond PBR material."""
    mat = bpy.data.materials.new(name="Diamond_Clear")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")

    # Set material properties for diamond
    bsdf.inputs["Base Color"].default_value = hex_to_rgb("#FFFACD")
    bsdf.inputs["Roughness"].default_value = 0.05
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["IOR"].default_value = 1.5  # Crucial for refraction
    bsdf.inputs["Transmission"].default_value = 1.0 # Make it transparent
    
    print("Created 'Diamond_Clear' material.")

def create_black_rubber():
    """Creates a Black Rubber PBR material with a tread pattern."""
    mat = bpy.data.materials.new(name="Rubber_Black")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    # Set base properties
    bsdf.inputs["Base Color"].default_value = hex_to_rgb("#1A1A1A")
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0

    # Create a tread pattern for the normal map
    wave_texture = nodes.new(type="ShaderNodeTexWave")
    wave_texture.inputs["Scale"].default_value = 10.0
    wave_texture.location = (-600, 0)

    noise_texture = nodes.new(type="ShaderNodeTexNoise")
    noise_texture.inputs["Scale"].default_value = 5.0
    noise_texture.location = (-600, -200)
    
    mix_rgb = nodes.new(type="ShaderNodeMixRGB")
    mix_rgb.blend_type = 'MIX'
    mix_rgb.inputs["Fac"].default_value = 0.7
    mix_rgb.location = (-300, 0)

    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.inputs["Strength"].default_value = 0.4
    bump_node.location = (-150, 0)

    mat.node_tree.links.new(wave_texture.outputs["Color"], mix_rgb.inputs["Color1"])
    mat.node_tree.links.new(noise_texture.outputs["Fac"], mix_rgb.inputs["Color2"])
    mat.node_tree.links.new(mix_rgb.outputs["Color"], bump_node.inputs["Height"])
    mat.node_tree.links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])
    
    print("Created 'Rubber_Black' material.")

def create_brushed_metal():
    """Creates a Brushed Metal PBR material."""
    mat = bpy.data.materials.new(name="Metal_Brushed")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    bsdf.inputs["Base Color"].default_value = hex_to_rgb("#C0C0C0")
    bsdf.inputs["Roughness"].default_value = 0.25
    bsdf.inputs["Metallic"].default_value = 1.0

    # Create a directional brushing pattern
    noise_texture = nodes.new(type="ShaderNodeTexNoise")
    noise_texture.inputs["Scale"].default_value = 150.0
    noise_texture.location = (-450, 0)

    mapping_node = nodes.new(type="ShaderNodeMapping")
    # This is the corrected line:
    mapping_node.inputs["Scale"].default_value[0] = 0.1 # Stretch noise on X-axis
    mapping_node.location = (-300, 0)

    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.inputs["Strength"].default_value = 0.2
    bump_node.location = (-150, 0)
    
    mat.node_tree.links.new(noise_texture.outputs["Fac"], mapping_node.inputs["Vector"])
    mat.node_tree.links.new(mapping_node.outputs["Vector"], bump_node.inputs["Height"])
    mat.node_tree.links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

    print("Created 'Metal_Brushed' material.")

def create_fabric_weave():
    """Creates a Fabric Weave PBR material."""
    mat = bpy.data.materials.new(name="Fabric_Weave")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1) # Default gray
    bsdf.inputs["Roughness"].default_value = 0.65
    bsdf.inputs["Metallic"].default_value = 0.0

    # Create a weave pattern using two wave textures
    wave_x = nodes.new(type="ShaderNodeTexWave")
    wave_x.inputs["Scale"].default_value = 40.0
    wave_x.bands_direction = 'X'
    wave_x.location = (-450, 100)

    wave_y = nodes.new(type="ShaderNodeTexWave")
    wave_y.inputs["Scale"].default_value = 40.0
    wave_y.bands_direction = 'Y'
    wave_y.location = (-450, -100)

    math_node = nodes.new(type="ShaderNodeMath")
    math_node.operation = 'MAXIMUM'
    math_node.location = (-300, 0)

    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.inputs["Strength"].default_value = 0.3
    bump_node.location = (-150, 0)

    mat.node_tree.links.new(wave_x.outputs["Fac"], math_node.inputs[0])
    mat.node_tree.links.new(wave_y.outputs["Fac"], math_node.inputs[1])
    mat.node_tree.links.new(math_node.outputs["Value"], bump_node.inputs["Height"])
    mat.node_tree.links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

    print("Created 'Fabric_Weave' material.")


# --- Main Execution ---
if __name__ == "__main__":
    # Clear existing materials to avoid duplicates if script is run multiple times
    for material in bpy.data.materials:
        # A check to avoid trying to remove the default 'Dots Stroke' material if it exists
        if material.name != 'Dots Stroke':
            bpy.data.materials.remove(material)
        
    print("--- Generating PBR Materials ---")
    create_polished_gold()
    create_clear_diamond()
    create_black_rubber()
    create_brushed_metal()
    create_fabric_weave()
    print("--- Material Generation Complete! ---")
