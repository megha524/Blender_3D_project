# Model Download and HDRI Setup Guide

## Part 1: Downloading GLB Models from Sketchfab

### Option A: Direct Download (Requires Sketchfab Account)

#### Model 1: Doji Diamond Ring
1. Visit: https://sketchfab.com/3d-models/doji-diamond-ring-297133c25c4b4d62b3237b05f800e323
2. Click "Download" button (top right)
3. Select format: **GLB (Binary glTF)**
4. Save to: `models/diamond-ring.glb`

#### Model 2: Earring Diamond
1. Visit: https://sketchfab.com/3d-models/earring-diamond-94db5e5434d14a9f87bbf3e5a5fd7dce
2. Click "Download" button
3. Select format: **GLB**
4. Save to: `models/earring.glb`

#### Model 3: Nike Shoe Unboxing
1. Visit: https://sketchfab.com/3d-models/nike-shoe-unboxing-animation-2a37e7725570445aa2a9c87b2a7d272a
2. Click "Download" button
3. Select format: **GLB**
4. Save to: `models/nike-shoe.glb`

### Option B: Using Sketchfab API (Automated)

If you have a Sketchfab API token, use this PowerShell script:

```powershell
# Sketchfab Download Script
$models = @(
    @{id = "297133c25c4b4d62b3237b05f800e323"; name = "diamond-ring.glb"},
    @{id = "94db5e5434d14a9f87bbf3e5a5fd7dce"; name = "earring.glb"},
    @{id = "2a37e7725570445aa2a9c87b2a7d272a"; name = "nike-shoe.glb"}
)

# Replace with your actual Sketchfab API token
$token = "YOUR_SKETCHFAB_TOKEN"

foreach ($model in $models) {
    $url = "https://api.sketchfab.com/v3/models/$($model.id)/download"
    $headers = @{"Authorization" = "Token $token"}
    
    Invoke-WebRequest -Uri $url -Headers $headers `
        -OutFile "models/$($model.name)"
    
    Write-Host "Downloaded: $($model.name)"
}
```

### Troubleshooting Downloads
- **Problem**: "Download button unavailable"
  - **Solution**: Model author may have disabled downloads. Look for alternative models or contact author
  
- **Problem**: "Wrong file format"
  - **Solution**: Always select GLB (Binary) format, not FBX, OBJ, or GLTF

- **Problem**: "File corrupted after download"
  - **Solution**: Re-download; ensure file is > 1 MB

---

## Part 2: Setting Up HDRI Environment

### What is HDRI?
HDRI (High Dynamic Range Image) is a 360° environment map that:
- Provides realistic lighting from all directions
- Creates believable reflections on metallic surfaces
- Simulates real-world lighting conditions for AR

### Option 1: Download Free HDRI from Polyhaven

#### Recommended HDRI for Jewelry (Diamond Ring, Earring)
1. Visit: https://polyhaven.com/hdris
2. Search: "studio" or "light studio"
3. Recommended: "Studio 01" or "Studio 016"
4. Download 4K version (EXR format recommended)
5. Save to: `textures/hdri/studio.exr`

**Why Studio HDRI?**
- Clean white background for jewelry visualization
- Directional key and fill lighting
- Minimizes reflections of unwanted environment
- Standard for jewelry product photography

#### Recommended HDRI for Nike Shoe (Product/AR Environment)
1. Search: "urban" or "street"
2. Recommended: "Tokyo Tower" or "Urban Roadside"
3. Download 4K version
4. Save to: `textures/hdri/urban.exr`

**Why Environment HDRI?**
- Realistic contextual lighting
- Believable reflections for AR integration
- Natural outdoor or urban setting

### Option 2: Download from Ambientcg

Alternative free HDRI source: https://ambientcg.com

Popular choices:
- "Kloofendal_43d" (outdoor, neutral)
- "Newport_Loft" (indoor, bright)
- "Odeon_01" (architectural)

### Option 3: Use Blender's Built-In HDRI

Blender includes default HDRI maps:
- Path: `Blender/data/studiolights/world/`
- Contains several basic studio and outdoor environments

### Importing HDRI into Blender

#### Method 1: Via Shading Workspace
1. Open Blender project
2. Switch to **Shading** workspace (top menu)
3. In shader editor, toggle world mode (small sphere icon)
4. Add node: `Shift+A` → Texture → Image Texture
5. Load image: Click "Open" → Select HDRI file
6. Connect to Background shader
7. Adjust strength (typically 1.0-3.0)

#### Method 2: Via World Properties
1. Go to **World Properties** panel (right side)
2. Click "Use Nodes"
3. Background node → Load image
4. Adjust energy value

### HDRI Settings for AR

```
Render Settings for AR Realism:
- HDRI Brightness: 1.5-2.0 (simulates outdoor daylight)
- Rotation: Z = 0° (or adjust to match light direction)
- Background Blur: 0.1 (defocus background, focus on model)
- Ambient Occlusion: Enable (for ground contact shadow)
```

### Creating Directory Structure

```powershell
# Create HDRI folder
New-Item -Path "textures/hdri" -ItemType Directory

# Download and organize
# Place all HDRI files in textures/hdri/
```

---

## Part 3: Organizing Downloaded Files

### Final Directory Structure

```
testing_3d_models/
├── models/
│   ├── diamond-ring.glb          ← Downloaded from Sketchfab
│   ├── earring.glb
│   └── nike-shoe.glb
│
├── textures/
│   ├── hdri/
│   │   ├── studio.exr            ← For jewelry
│   │   └── urban.exr             ← For shoe
│   │
│   ├── gold_polished/
│   │   ├── albedo.png
│   │   ├── roughness.png
│   │   ├── metallic.png
│   │   └── normal.png
│   │
│   ├── diamond/
│   │   ├── albedo.png
│   │   ├── roughness.png
│   │   └── normal.png
│   │
│   └── rubber/
│       ├── albedo.png
│       ├── roughness.png
│       └── normal.png
│
├── blender/
│   ├── diamond_ring_pbr.blend
│   ├── earring_pbr.blend
│   └── nike_shoe_pbr.blend
│
└── documentation/
    ├── MATERIAL_ANALYSIS.md
    ├── BLENDER_WORKFLOW.md
    ├── HDRI_SETUP.md
    └── blender_pbr_generator.py
```

---

## Part 4: File Size and Format Recommendations

### Texture Export Settings

#### For HDRI
```
Format: EXR (32-bit float, HDR)
Compression: ZIP (lossless)
Resolution: 4K (4096×4096) or 2K (2048×2048)
Size: ~15-30 MB per file
```

#### For Albedo Maps
```
Format: PNG (8-bit sRGB)
Compression: Maximum
Resolution: 2K or 4K
Size: ~1-3 MB per texture
Color Space: sRGB (NOT linear)
```

#### For Roughness/Metallic/Normal
```
Format: PNG (8-bit linear)
Compression: Maximum
Resolution: Same as Albedo (2K or 4K)
Size: ~1-3 MB per texture
Color Space: Linear (NOT sRGB)
```

### Mobile AR Optimization
- **Max Texture Resolution**: 2K (2048×2048)
- **Max Total Texture Memory**: 50 MB per model
- **Format**: PNG (lossless) or WebP (lossy, smaller)
- **Packed Textures**: Combine R+G+B channels

---

## Part 5: Blender HDRI Node Setup

### Complete World Shader Setup

```
Node Configuration:
1. Mapping Node
   - Location: (X, Y, Z)
   - Rotation Z: [adjust for light direction]
   - Scale: (1, 1, 1)

2. Texture Coordinate
   - Generated coordinate

3. Image Texture
   - Image: [Load HDRI file]
   - Interpolation: Linear

4. Background Shader
   - Color: [Connected from Image Texture]
   - Strength: 2.0 (bright studio)

5. Material Output
   - Surface: [Connected from Background]

Connections:
Texture Coordinate.Generated → Mapping.Vector
Mapping.Vector → Image Texture.Vector
Image Texture.Color → Background.Color
Background.Background → Material Output.Surface
```

### Rotating HDRI for Light Direction

1. In Mapping node, adjust **Rotation Z**
2. Live preview updates lighting direction
3. For jewelry: Z = 45° (diagonal light)
4. For product: Z = 0° or 90° (depending on desired effect)

---

## Part 6: Troubleshooting

### Problem: HDRI file not loading
- **Solution**: Ensure file format is supported (EXR, HDR, PNG, JPG)
- **Solution**: Check file path has no special characters

### Problem: HDRI looks washed out
- **Solution**: Increase Background Strength to 2.0-3.0
- **Solution**: Check color management (Filmic recommended)

### Problem: Model looks too dark with HDRI
- **Solution**: Add key light (Sun lamp, energy 2.0)
- **Solution**: Enable Ambient Occlusion

### Problem: Model reflections look wrong
- **Solution**: Verify material Metallic/Roughness values
- **Solution**: Disable Ambient Occlusion in material properties
- **Solution**: Increase IOR for reflective surfaces

---

## Next Steps

1. ✅ Download the three GLB models
2. ✅ Download studio HDRI for jewelry
3. ✅ Download urban HDRI for shoe
4. ✅ Organize in folder structure
5. → Open Blender and follow BLENDER_WORKFLOW.md
6. → Apply PBR materials to each model
7. → Test in real-time viewport

