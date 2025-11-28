"""
Blender Python Script: Procedural PBR Material Generator
For use in Blender's scripting console or as addon

This script creates procedural PBR materials in Blender for:
- Polished Gold (jewelry)
- Diamond/Crystal (clear, highly refractive)
- Rubber (textured, matte)
- Metallic (polished, brushed)
- Fabric/Mesh (woven texture)

Usage:
1. Open Blender
2. Switch to Shading workspace
3. Open Scripting console
4. Paste this script
5. Run (Alt+P)
"""

import bpy
from mathutils import Vector

# ===== MATERIAL 1: POLISHED GOLD =====
def create_gold_material(name="Gold_Polished"):
    """Create polished gold material with procedural textures"""
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Principled BSDF
    principal = nodes.new(type="ShaderNodeBsdfPrincipled")
    principal.inputs["Base Color"].default_value = (0.839, 0.647, 0.455, 1.0)  # Gold color
    principal.inputs["Metallic"].default_value = 1.0
    principal.inputs["Roughness"].default_value = 0.35
    
    # Color Ramp for Roughness variation
    color_ramp = nodes.new(type="ShaderNodeValRamp")
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[1].position = 0.4
    
    # Noise Texture for Roughness
    noise_rough = nodes.new(type="ShaderNodeTexNoise")
    noise_rough.inputs["Scale"].default_value = 15
    noise_rough.inputs["Detail"].default_value = 5
    
    # Noise Texture for Normal
    noise_normal = nodes.new(type="ShaderNodeTexNoise")
    noise_normal.inputs["Scale"].default_value = 50
    noise_normal.inputs["Detail"].default_value = 3
    
    # Bump to Normal
    bump = nodes.new(type="ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.3
    
    # Output
    output = nodes.new(type="ShaderNodeOutputMaterial")
    
    # Connect nodes
    links.new(noise_rough.outputs["Fac"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], principal.inputs["Roughness"])
    links.new(noise_normal.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principal.inputs["Normal"])
    links.new(principal.outputs["BSDF"], output.inputs["Surface"])
    
    return mat


# ===== MATERIAL 2: DIAMOND/CLEAR =====
def create_diamond_material(name="Diamond_Clear"):
    """Create realistic diamond material with refraction"""
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Principled BSDF
    principal = nodes.new(type="ShaderNodeBsdfPrincipled")
    principal.inputs["Base Color"].default_value = (1.0, 0.98, 0.8, 1.0)  # Near white
    principal.inputs["Metallic"].default_value = 0.0
    principal.inputs["Roughness"].default_value = 0.05
    principal.inputs["IOR"].default_value = 1.5
    
    # Output
    output = nodes.new(type="ShaderNodeOutputMaterial")
    
    # Connect
    links.new(principal.outputs["BSDF"], output.inputs["Surface"])
    
    return mat


# ===== MATERIAL 3: RUBBER =====
def create_rubber_material(name="Rubber_Black"):
    """Create textured rubber material with tread pattern"""
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Principled BSDF
    principal = nodes.new(type="ShaderNodeBsdfPrincipled")
    principal.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)  # Deep black
    principal.inputs["Metallic"].default_value = 0.0
    principal.inputs["Roughness"].default_value = 0.85
    
    # Color Ramp for Roughness variation
    color_ramp = nodes.new(type="ShaderNodeValRamp")
    color_ramp.color_ramp.elements[0].position = 0.75
    color_ramp.color_ramp.elements[1].position = 0.95
    
    # Noise for Roughness
    noise_rough = nodes.new(type="ShaderNodeTexNoise")
    noise_rough.inputs["Scale"].default_value = 30
    noise_rough.inputs["Detail"].default_value = 4
    
    # Wave Texture for tread (directional)
    wave = nodes.new(type="ShaderNodeTexWave")
    wave.inputs["Scale"].default_value = 100
    wave.wave_type = 'SINE'
    
    # Noise for tread detail
    noise_tread = nodes.new(type="ShaderNodeTexNoise")
    noise_tread.inputs["Scale"].default_value = 50
    
    # Mix for combined tread
    mix_tread = nodes.new(type="ShaderNodeMix")
    mix_tread.data_type = 'FLOAT'
    mix_tread.inputs["A"].default_value = 0.5
    mix_tread.inputs["B"].default_value = 0.5
    
    # Bump
    bump = nodes.new(type="ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.5
    
    # Output
    output = nodes.new(type="ShaderNodeOutputMaterial")
    
    # Connect
    links.new(noise_rough.outputs["Fac"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], principal.inputs["Roughness"])
    links.new(wave.outputs["Fac"], mix_tread.inputs["A"])
    links.new(noise_tread.outputs["Fac"], mix_tread.inputs["B"])
    links.new(mix_tread.outputs["Result"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principal.inputs["Normal"])
    links.new(principal.outputs["BSDF"], output.inputs["Surface"])
    
    return mat


# ===== MATERIAL 4: BRUSHED METAL =====
def create_brushed_metal_material(name="Metal_Brushed"):
    """Create brushed metal material (for prongs, eyelets, etc.)"""
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Principled BSDF
    principal = nodes.new(type="ShaderNodeBsdfPrincipled")
    principal.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)  # Silver
    principal.inputs["Metallic"].default_value = 1.0
    principal.inputs["Roughness"].default_value = 0.25
    
    # Directional brushing pattern
    noise = nodes.new(type="ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 100
    noise.inputs["Detail"].default_value = 2
    
    # Color ramp for brushing effect
    color_ramp = nodes.new(type="ShaderNodeValRamp")
    color_ramp.color_ramp.elements[0].position = 0.2
    color_ramp.color_ramp.elements[1].position = 0.3
    
    # Bump
    bump = nodes.new(type="ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.2
    
    # Output
    output = nodes.new(type="ShaderNodeOutputMaterial")
    
    # Connect
    links.new(noise.outputs["Fac"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principal.inputs["Normal"])
    links.new(principal.outputs["BSDF"], output.inputs["Surface"])
    
    return mat


# ===== MATERIAL 5: WOVEN FABRIC =====
def create_fabric_material(name="Fabric_Weave"):
    """Create woven fabric material (for shoe mesh, etc.)"""
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Principled BSDF
    principal = nodes.new(type="ShaderNodeBsdfPrincipled")
    principal.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)  # Gray base
    principal.inputs["Metallic"].default_value = 0.0
    principal.inputs["Roughness"].default_value = 0.65
    
    # Wave texture for weave pattern
    wave = nodes.new(type="ShaderNodeTexWave")
    wave.inputs["Scale"].default_value = 150
    wave.wave_type = 'SAW'
    
    # Noise for fiber detail
    noise = nodes.new(type="ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 50
    noise.inputs["Detail"].default_value = 4
    
    # Mix textures
    mix = nodes.new(type="ShaderNodeMix")
    mix.data_type = 'FLOAT'
    mix.inputs["A"].default_value = 0.5
    mix.inputs["B"].default_value = 0.5
    
    # Bump
    bump = nodes.new(type="ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.4
    
    # Output
    output = nodes.new(type="ShaderNodeOutputMaterial")
    
    # Connect
    links.new(wave.outputs["Fac"], mix.inputs["A"])
    links.new(noise.outputs["Fac"], mix.inputs["B"])
    links.new(mix.outputs["Result"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principal.inputs["Normal"])
    links.new(principal.outputs["BSDF"], output.inputs["Surface"])
    
    return mat


# ===== MAIN EXECUTION =====
def create_all_materials():
    """Create all PBR materials"""
    materials = {
        "Gold_Polished": create_gold_material(),
        "Diamond_Clear": create_diamond_material(),
        "Rubber_Black": create_rubber_material(),
        "Metal_Brushed": create_brushed_metal_material(),
        "Fabric_Weave": create_fabric_material(),
    }
    
    print("✓ Created PBR Materials:")
    for name, mat in materials.items():
        print(f"  - {name}")
    
    return materials


# Run on script execution
if __name__ == "__main__":
    materials = create_all_materials()
    print(f"\nTotal: {len(materials)} materials created")
    print("Assign materials to objects in Material Properties panel")
