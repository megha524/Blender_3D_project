# Texture Packing and Optimization Guide

## Overview: Packed Texture Atlasing

Texture packing combines multiple grayscale texture maps into a single RGBA image, reducing memory usage by 50-75%.

### Standard Packing Strategy

**Single Packed Texture (RGBA):**
```
Channel R: Roughness (0=smooth, 255=rough)
Channel G: Metallic (0=non-metal, 255=metal)
Channel B: Ambient Occlusion (optional, 0=shadow, 255=lit)
Channel A: Height/Displacement (optional, for parallax)
```

**Benefits:**
- ✓ 50% memory savings (2 maps → 1 map)
- ✓ Single texture bind instead of two
- ✓ Faster shader execution
- ✓ Ideal for mobile AR (WebGL constraint)

**Trade-offs:**
- Slight loss of precision per channel (8-bit instead of full channel)
- Requires custom shader to unpack channels
- More complex workflow during creation

---

## Part 1: Creating Individual Maps

### Step 1: Generate Roughness Map

**In Blender Shader Editor:**

```
Node Setup for Roughness:
1. Noise Texture (Perlin)
   - Scale: 20
   - Detail: 5
   - Input: Generated coordinates

2. ColorRamp
   - Min position: 0.25
   - Max position: 0.75
   - Adjust colors for desired roughness range

3. File Output Node
   - Name: "roughness"
   - Format: PNG 8-bit Linear

Connection:
Noise → ColorRamp → File Output
```

### Step 2: Generate Metallic Map

**For Simple Binary Metallic:**

```
Node Setup:
1. Noise Texture (Value)
   - Scale: 5
   - Lacunarity: 2.0
   - Used as mask for metallic areas

2. ColorRamp
   - Min: Black (0.0)
   - Max: White (1.0)
   - Threshold control

3. File Output Node
   - Name: "metallic"

Connection:
Noise → ColorRamp → File Output
```

**For Gradient Metallic (Semi-reflective):**

```
Instead of binary, use ColorRamp with intermediate values:
- 0.0: Non-metallic (rubber, fabric)
- 0.3: Semi-metallic (worn metal)
- 1.0: Polished metal (jewelry)
```

### Step 3: Generate Ambient Occlusion

**Method A: Baking from Geometry (Recommended)**

1. Select object in Blender
2. Bake → Type: Ambient Occlusion
3. Save baked texture as "ambient_occlusion.png"

**Method B: Procedural Generation**

```
Node Setup:
1. Noise Texture (Perlin)
   - Scale: 50
   - Detail: 8
   - Creates cavity shadows

2. ColorRamp
   - Adjust to create shadow effect
   - Higher values in cavities

3. File Output Node
   - Name: "ambient_occlusion"
```

### Step 4: Export Individual Maps

**Blender Compositor Method:**

1. Switch to **Compositor** workspace
2. Enable "Use Nodes" in compositor
3. Add File Output nodes for each map
4. In Render Properties:
   - Format: PNG
   - Color Depth: 8-bit
   - Color Space: Linear (for roughness/metallic), sRGB (for AO)
5. Render: `F12`
6. Maps automatically save to render output folder

---

## Part 2: Combining Maps into Packed Texture

### Method A: Using Blender (Node-Based)

**Setup for Packing Roughness + Metallic:**

```
Nodes Required:
1. Image Texture (Roughness)
   - Load "roughness.png"

2. Image Texture (Metallic)
   - Load "metallic.png"

3. Separate Color (Roughness)
   - Input: Roughness image
   - Output: Separate into R, G, B channels

4. Separate Color (Metallic)
   - Input: Metallic image

5. Combine Color
   - R channel: Roughness (from Separate)
   - G channel: Metallic (from Separate)
   - B channel: Ambient Occlusion (from Separate, if available)
   - A channel: (leave empty or use height map)

6. File Output
   - Name: "packed_roughness_metallic.png"

Connections:
Roughness Image → Separate Color
Metallic Image → Separate Color
Separate(R) → Combine(R)
Separate(G) → Combine(G)
Combine → File Output
```

### Method B: Using Python Script

**Blender Python Script for Packing:**

```python
import bpy
from PIL import Image
import numpy as np

def pack_textures(roughness_path, metallic_path, output_path):
    """
    Combine Roughness and Metallic into packed RGBA texture
    
    Args:
        roughness_path: Path to roughness map (grayscale PNG)
        metallic_path: Path to metallic map (grayscale PNG)
        output_path: Path to save packed texture
    """
    
    # Load images
    roughness_img = Image.open(roughness_path).convert('L')
    metallic_img = Image.open(metallic_path).convert('L')
    
    # Ensure same size
    size = roughness_img.size
    metallic_img = metallic_img.resize(size, Image.Resampling.LANCZOS)
    
    # Convert to numpy arrays
    rough_array = np.array(roughness_img)
    metal_array = np.array(metallic_img)
    
    # Create RGBA packed texture
    packed = np.zeros((*rough_array.shape, 4), dtype=np.uint8)
    packed[:, :, 0] = rough_array  # R = Roughness
    packed[:, :, 1] = metal_array  # G = Metallic
    packed[:, :, 2] = 255         # B = 1.0 (neutral)
    packed[:, :, 3] = 255         # A = 1.0 (full opacity)
    
    # Save packed texture
    packed_img = Image.fromarray(packed, 'RGBA')
    packed_img.save(output_path, 'PNG')
    
    print(f"✓ Packed texture saved: {output_path}")
    return output_path

# Usage in Blender console:
# pack_textures('textures/roughness.png', 'textures/metallic.png', 'textures/packed_rm.png')
```

### Method C: Using External Tools

**Using Substance Painter:**
1. Import base model
2. Create Roughness and Metallic layers
3. Export: Texture Set Settings → Output Template
4. Select "PBR MetalRough" preset
5. Roughness exports to R, Metallic to G automatically

**Using TextureLab (Web-based):**
1. Upload individual texture maps
2. Drag R to Roughness
3. Drag G to Metallic
4. Export as PNG

---

## Part 3: Using Packed Textures in Shader

### Blender Shader Setup (Unpacking)

**Node Graph for Unpacking:**

```
1. Image Texture (Packed)
   - Load: "packed_roughness_metallic.png"
   - Interpolation: Linear

2. Separate Color
   - Input: Packed Image
   - Output: Separate R, G, B, A

3. Principled BSDF
   - Roughness: Connect from Separate.R
   - Metallic: Connect from Separate.G

Complete Setup:
Packed Image → Separate Color
Separate.R → Principled.Roughness
Separate.G → Principled.Metallic
Principled → Material Output
```

### Shader Code (for GLSL export)

```glsl
// Unpack texture in fragment shader
#version 330

uniform sampler2D packedTexture;
in vec2 uv;

void main() {
    vec4 packed = texture(packedTexture, uv);
    
    float roughness = packed.r;    // R channel = roughness
    float metallic = packed.g;     // G channel = metallic
    float ambientOcclusion = packed.b;  // B channel = AO
    
    // Apply to material
    // ... material calculations using roughness, metallic, AO
}
```

---

## Part 4: Multi-Material Packing Strategy

For projects with 3+ materials, create material-specific packed atlases.

### Example: Nike Shoe with 5 Materials

**Packing Approach:**

```
Packed Texture 1 (Rubber Sole):
R: Roughness (high, 0.8-0.9)
G: Metallic (0, non-metal)
B: AO (varies)
A: Height (tread depth)

Packed Texture 2 (Mesh Fabric):
R: Roughness (medium, 0.6-0.7)
G: Metallic (0, non-metal)
B: AO (slight)
A: Weave pattern

Packed Texture 3 (Metallic Eyelets):
R: Roughness (low, 0.2)
G: Metallic (1.0, full metal)
B: AO (minimal)
A: Height (cylindrical shape)

Packed Texture 4 (Synthetic Leather):
R: Roughness (0.3-0.5)
G: Metallic (0, non-metal)
B: AO (medium)
A: Normal detail
```

**Benefits:**
- Specific optimization per material type
- Easier to maintain and update
- Better performance than individual maps

---

## Part 5: Export and Integration

### Exporting Packed Texture from Blender

**Step 1: Add File Output Node**
1. In Shader Editor, add File Output node
2. Connect Combine Color output to File Output.Image
3. Name: "packed_roughness_metallic"

**Step 2: Set Output Format**
1. Render Properties → Output
2. Format: PNG
3. Color Depth: 8-bit
4. Color Space: Linear

**Step 3: Render**
1. Press `F12` to render
2. Image automatically saves to:
   - `//textures/packed_roughness_metallic.png`

### Verify Packed Texture

Open packed texture in image viewer:
- **R Channel (Roughness)**: Appears as gray tones (darker = smoother)
- **G Channel (Metallic)**: Appears as colored (red-tinted areas = metallic)
- **B Channel (AO)**: Appears as darker in crevices

---

## Part 6: Performance Impact

### Memory Savings Comparison

```
Before Packing (Individual Maps):
- Roughness: 2K PNG = 2.1 MB
- Metallic: 2K PNG = 1.8 MB
- Normal Map: 2K PNG = 2.3 MB
- Total: 6.2 MB per material

After Packing (Roughness + Metallic):
- Packed RM: 2K PNG = 1.9 MB
- Normal Map: 2K PNG = 2.3 MB
- Total: 4.2 MB per material

Savings: 32% memory reduction
```

### Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Texture Memory | 100% | 50-67% | 33-50% ↓ |
| Texture Lookups | 3-4 per shader | 1-2 per shader | 50-75% ↓ |
| Shader Complexity | Medium | Low | 20% ↓ |
| Load Time | Baseline | -15% | 15% ↑ |

---

## Part 7: Advanced: Three-Channel Packing

**Maximum Optimization (Roughness + Metallic + AO):**

```
R: Roughness (0-255)
G: Metallic (0-255)
B: Ambient Occlusion (0-255)
A: (Reserve for future use)
```

**Shader Unpacking:**
```glsl
vec3 packed = texture(packedTexture, uv).rgb;
float roughness = packed.r / 255.0;
float metallic = packed.g / 255.0;
float ambientOcclusion = packed.b / 255.0;
```

---

## Deliverables Checklist

- [ ] Individual Roughness map created
- [ ] Individual Metallic map created
- [ ] Ambient Occlusion map created (optional)
- [ ] Packed texture generated (RGBA PNG)
- [ ] Packed texture tested in Blender
- [ ] Shader unpacking nodes verified
- [ ] File size optimized (< 2 MB per 2K texture)
- [ ] Documentation updated with packing info

---

## Next Steps

1. Generate individual Roughness and Metallic maps
2. Combine using chosen method (Blender nodes / Python / Substance)
3. Export as PNG (8-bit, linear color space)
4. Test unpacking in shader
5. Verify memory savings
6. Use in final AR scene

