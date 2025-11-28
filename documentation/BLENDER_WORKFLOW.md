# Blender PBR Material Setup Guide

## Quick Start

### Prerequisites
- Blender 3.4+ installed
- Downloaded GLB models in `models/` folder
- HDRI image (download from Polyhaven or provided)

### Recommended Settings in Blender
```
Render Engine: Eevee or Cycles (both support PBR)
Color Management: Filmic (Blender default)
Device: GPU (if available)
Resolution: 1920x1440 (AR-typical aspect ratio)
```

---

## Part 1: Scene Setup for AR Environment

### 1.1 Create Base Scene
1. Open Blender → Start with General project
2. Delete default cube
3. Set World background to HDRI:
   - Go to Shading (top menu) → Switch to "World" mode
   - Add Background shader
   - Download HDRI from: https://polyhaven.com/hdris (e.g., "Rural_crossroads_01")
   - Load HDRI into image texture node
   - Connect to Background shader

### 1.2 Set Up Lighting
1. Add Key Light: `Shift+A` → Light → Sun Lamp
   - Rotation: X=45°, Z=45°
   - Energy: 2.0
   - Shadow: Enable soft shadows

2. Optional Fill Light: Add second softer sun lamp
   - Rotation: X=25°, Z=180°
   - Energy: 0.5

### 1.3 Configure Camera
1. Add Camera: `Shift+A` → Camera
2. Position for AR perspective
3. Set as active camera: Select camera → `Ctrl+Numpad 0`

### 1.4 Add Background Plane (Optional)
1. Add plane: `Shift+A` → Mesh → Plane
2. Scale large and position behind model
3. Assign neutral gray material (RGB: 0.5, 0.5, 0.5)

---

## Part 2: Importing Models

### 2.1 Import First Model
1. `File` → `Import` → `glTF 2.0 (.glb/.gltf)`
2. Select: `diamond-ring.glb`
3. Set scale and position appropriately
4. Press `Import glTF 2.0`

### 2.2 Inspect Imported Model
1. Check material slots (should be mostly empty)
2. Identify different mesh objects (select all: `A`, then `Tab` to enter edit mode)
3. Take note of material naming from original model

---

## Part 3: Creating PBR Materials - Material 1: Polished Gold

### 3.1 Create New Material
1. Select model object
2. In Shading workspace (top menu)
3. New Material → Name: "Gold_Polished"

### 3.2 Base Shader Node Setup
1. Add Principled BSDF (if not present)
2. Replace Diffuse BSDF with Principled BSDF

### 3.3 Gold Material Nodes

**Step 1: Base Color (Albedo)**
```
Node Setup:
- ColorRamp node → Input "Fac" = 0
  - Color 1: #D4A574 (warm gold)
  - Color 2: #E8D4B8 (light gold highlight)
- Connect to Principled BSDF "Base Color"
```

**Step 2: Roughness**
```
Node Setup:
- Noise Texture
  - Scale: 15
  - Detail: 5
- ColorRamp
  - Input values: min 0.3, max 0.4 (polished gold)
- Connect to Principled BSDF "Roughness"
```

**Step 3: Metallic**
```
Node Setup:
- Connect static value 1.0 to "Metallic" input
  (All gold is metallic)
```

**Step 4: Normal Map**
```
Node Setup:
- Noise Texture
  - Scale: 50
  - Detail: 3
- Bump Texture
  - Strength: 0.3
- Convert to Normal node
- Connect to Principled BSDF "Normal"
```

### 3.4 Complete Node Graph for Gold
```
ColorRamp → Principled BSDF.Base Color
Noise (scaled 15) → ColorRamp → Principled BSDF.Roughness
1.0 (value) → Principled BSDF.Metallic
Noise (scaled 50) → Bump → Normal → Principled BSDF.Normal
```

---

## Part 4: Creating PBR Materials - Material 2: Diamond

### 4.1 Create Material: "Diamond_Clear"

### 4.2 Diamond Material Nodes

**Step 1: Base Color**
```
- White color (#FFFACD - very light yellow)
- Connect directly to Principled BSDF "Base Color"
```

**Step 2: Roughness**
```
- Static value: 0.05 (extremely smooth)
- Connect to Principled BSDF "Roughness"
```

**Step 3: Metallic**
```
- Static value: 0.0 (non-metallic)
```

**Step 4: IOR (Index of Refraction)**
```
- Static value: 1.5 (diamond's refractive index)
- Connect to Principled BSDF "IOR"
```

**Step 5: Normal Map**
```
- Optional: Very subtle noise at scale 100
- Strength: 0.1 (minimal for perfect clarity)
```

### 4.3 Render Settings for Transparency
- For Eevee: Enable "Refraction" in material blend mode
- For Cycles: Already handles refraction correctly

---

## Part 5: Creating PBR Materials - Material 3: Rubber Sole

### 5.1 Create Material: "Rubber_Black"

### 5.2 Rubber Material Nodes

**Step 1: Base Color**
```
- Deep black (#1A1A1A)
- Add slight variation with Noise
- ColorRamp to add micro-variation
```

**Step 2: Roughness**
```
- Noise Texture (Perlin or Value)
  - Scale: 30
  - Detail: 4
- ColorRamp: min 0.75, max 0.95
- This creates natural rubber texture variation
```

**Step 3: Metallic**
```
- Static value: 0.0 (rubber is non-metallic)
```

**Step 4: Normal Map (Tread Pattern)**
```
- Wave Texture (for directional tread)
  - Scale: 100
  - Type: Sine
- Combine with Noise Texture
- Bump strength: 0.5
- Convert to Normal
```

---

## Part 6: Assigning Materials to Mesh Objects

### 6.1 Material Slots
1. Select mesh object (e.g., "Ring_Band")
2. In Material Properties panel
3. New Slot → Assign material "Gold_Polished"
4. Press "Assign" button

### 6.2 Repeat for All Objects
- Gold_Band → Gold_Polished
- Diamond_Stone → Diamond_Clear
- Prongs → Gold_Polished (or create separate brushed metal)

### 6.3 Switch to Material Preview
1. Viewport shading: Click sphere icon (third from right)
2. Select "Material Preview" or "Rendered" mode
3. Verify materials look correct

---

## Part 7: Advanced - Packed Texture Optimization

### 7.1 Create Packed Roughness+Metallic Texture

**Separate into channels:**
1. Add Separate RGB node for Roughness map
2. Add Separate RGB node for Metallic map
3. Use Combine RGB node to pack:
   - R channel: Roughness
   - G channel: Metallic
   - B channel: AO (Ambient Occlusion, if available)

**Example Node Tree:**
```
Noise (Roughness) → Separate RGB
Static 1.0 (Metallic) → Channel G
Combine RGB (R=Roughness, G=Metallic) → Image Texture Export
```

### 7.2 Export Packed Texture
1. Add File Output node
2. Connect packed texture to it
3. Render → Bake textures (or manually export)
4. Save as PNG in `textures/` folder

---

## Part 8: Animation - State Change with Emissive

### 8.1 Example: Diamond Ring - Ring Opening/Rotating

**Setup:**
1. Select Ring_Band object
2. Set keyframe at frame 1:
   - Rotation Z = 0°
   - Insert keyframe: `I` → Rotation

3. Move to frame 120
4. Rotate ring 360°
5. Insert keyframe: `I` → Rotation

**Add Emissive Glow:**
1. Edit material for "Gold_Polished"
2. Add second material output (hold Shift, drag from Principled)
3. Enable Emission shader for selected keyframes:
   - Add Emission shader
   - Color: Yellow (#FFFF00)
   - Strength: Animate from 0 to 2 over frames 60-120
4. Use Mix Shader to blend between normal and emissive

**Alternative: Nike Shoe Heating Animation**
- Metallic eyelets glow red (#FF4500)
- Emissive strength increases from frame 1-180
- Uses same approach with Emission shader

### 8.2 Set Up Animation
1. Switch to Animation workspace
2. View Action Editor
3. Create new Action: "Diamond_Rotation"
4. Configure playback FPS (typically 24 or 30)
5. Set End Frame: 240

### 8.3 Preview Animation
1. Press spacebar to play in 3D viewport
2. Adjust keyframes as needed
3. Export as video or image sequence if needed

---

## Part 9: Final Render Settings

### For Eevee (Real-Time Engine)
```
Render Properties:
- Ambient Occlusion: Enable
- Bloom: Enable (intensity 0.1)
- Depth of Field: Optional (depth 0.1)
- Motion Blur: Optional
- Subsurface Scattering: Disable (performance)

Material Properties:
- Blend Mode: Alpha Blend (for transparency)
- Shadow Mode: Hashed (for performance)
```

### For Cycles (Offline Quality)
```
Render Properties:
- Samples: 256 (high quality)
- Denoise: Enable OptiX/OpenImageDenoise
- Resolution: 1920×1440
- Format: PNG (lossless)
```

---

## Part 10: Export and Validation

### 10.1 Bake Textures to Images
1. Mark all texture nodes as "Use as Render" (orange outline)
2. Add Image Texture nodes
3. Bake render (Cycles) or use compositor (Eevee)
4. Save to `textures/` folder

### 10.2 Export Final Model
1. Select all objects with materials
2. `File` → `Export` → `glTF 2.0 (.glb/.gltf)`
3. Save to `blender/` folder as "model_with_pbr.glb"
4. Check "Include Materials"
5. Check "Bake Animation"

### 10.3 Validation Checklist
- [ ] All materials appear photorealistic in viewport
- [ ] HDRI reflections visible on metallic surfaces
- [ ] Rough materials have appropriate micro-detail
- [ ] Animation plays correctly
- [ ] Emissive materials glow as intended
- [ ] File size reasonable for AR (< 50 MB total)

---

## Troubleshooting

### Problem: Materials look too dark
- **Solution**: Increase sun lamp energy or adjust HDRI brightness

### Problem: Metallic surfaces don't reflect
- **Solution**: Verify Principled BSDF "Metallic" = 1.0; check viewport shading

### Problem: Normal maps look inverted
- **Solution**: Use normal map node instead of bump; check normal direction

### Problem: Animation exports poorly
- **Solution**: Ensure all animation is in single Action; bake constraints before export

---

## Next: Create Blender Project Files
See example setup in `blender/` folder for each model.

