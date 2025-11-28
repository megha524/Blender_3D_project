# Animation and Emissive Material Guide

## Overview

This guide covers creating state-change animations and emissive materials for AR-ready models. Examples include:
- Diamond ring rotating with glowing prongs
- Jewelry with heating effects
- Nike shoe with dynamic lighting
- Camera shutter opening
- Metal heating and cooling effects

---

## Part 1: Basic Animation Setup in Blender

### 1.1 Enable Animation Mode

1. Switch to **Animation** workspace (top menu)
2. View available panels:
   - Timeline (bottom)
   - Dope Sheet (left)
   - Action Editor
   - Graph Editor

### 1.2 Set Frame Range

1. Properties panel (right) → Scene Properties
2. Timeline:
   - **Start Frame**: 1
   - **End Frame**: 240 (10 seconds at 24 fps)
   - **Frame Rate**: 24 fps (standard for video)

### 1.3 Preview Animation

1. In Timeline, press **Spacebar** to play
2. Or press **Shift+Spacebar** for full-screen playback

---

## Part 2: Diamond Ring Rotation Animation

### 2.1 Rotate Object Animation

**Setup:**

1. Select Diamond Ring object
2. Move to frame 1: Click in Timeline at frame 1
3. Insert initial keyframe:
   - Press `I` (Insert Keyframe menu)
   - Select "Rotation"
   - Confirm

**Result:** Keyframe at frame 1 with rotation 0°

### 2.2 Create Rotation Keyframe

1. Move to frame 121 (middle of animation)
2. In Transform Properties (N-key), set:
   - Rotation Z: 180°
   - Insert keyframe: `I` → Rotation

3. Move to frame 240 (end)
4. Set Rotation Z: 360°
5. Insert keyframe: `I` → Rotation

**Result:** Smooth 360° rotation over 240 frames (10 seconds)

### 2.3 Adjust Animation Curve

1. Open **Graph Editor** (bottom panel)
2. Select "Rotation" curve in channel list
3. Adjust interpolation:
   - Click keyframe handle
   - Make smooth for linear rotation
   - Or add easing for dynamic rotation

**Linear Interpolation (Constant Speed):**
- Select keyframes
- Press `Shift+H` → Linear

**Easing (Slower → Faster → Slower):**
- Select keyframes
- Press `Tab` → Bezier
- Adjust handles for curve

---

## Part 3: Emissive Material Setup

### 3.1 Create Emissive Shader

**For: Diamond Ring Prongs Glowing**

1. Select Ring object
2. Switch to **Shading** workspace
3. Create new material: "Prongs_Emissive"

### 3.2 Emissive Node Graph

```
Node Setup:

1. Principled BSDF (Base material)
   - Base Color: #C0C0C0 (silver)
   - Roughness: 0.2
   - Metallic: 1.0

2. Emission Shader
   - Color: #FFFF00 (yellow/gold glow)
   - Strength: 2.0 (initial)

3. Mix Shader
   - Shader A: Principled BSDF
   - Shader B: Emission Shader
   - Fac (Factor): [Animated 0 to 1]

4. Material Output
   - Surface: [Connected from Mix Shader]

Connections:
Principled → Mix Shader.Shader A
Emission → Mix Shader.Shader B
Mix Shader → Material Output
```

### 3.3 Animate Emission Strength

**Method A: Using Animated Value Node**

1. Add **Math** node (or Value node)
2. Connect to Mix Shader "Fac" input
3. Keyframe the value:
   - Frame 1: Value = 0 (no emission)
   - Frame 120: Value = 0.5 (medium glow)
   - Frame 240: Value = 1.0 (full emission)

**Method B: Directly Animate Emission Strength**

1. Select Emission shader
2. Hover over "Strength" slider
3. Insert keyframe: `I` (right-click → Insert Keyframe)
4. Frame 1: Strength = 0
5. Frame 240: Strength = 3.0

### 3.4 Create Heating Effect (Advanced)

**Example: Metal Heating and Cooling**

```
Animation Timeline:
- Frame 1-60: Cold (no emission)
- Frame 60-120: Heating (color changes red)
- Frame 120-180: Hot (full yellow emission)
- Frame 180-240: Cooling (emission fades)

Emission Color Keyframes:
Frame 1: Black (#000000) - no glow
Frame 60: Dark Red (#330000) - starting heat
Frame 120: Bright Red (#FF4500) - hot
Frame 180: Orange (#FF8C00) - cooling
Frame 240: Dark Red (#330000) - cooled

Emission Strength Keyframes:
Frame 1: 0.0
Frame 60: 0.5
Frame 120: 3.0
Frame 180: 1.5
Frame 240: 0.0
```

**Implementation:**

1. Add Color Ramp node before Emission Color
2. Animate ColorRamp position (keyframe index slider)
3. Or directly keyframe Emission Color:
   - Right-click color swatch
   - "Insert Keyframe"
   - Change color at different frames

---

## Part 4: Diamond Ring with Animation and Glow

### 4.1 Complete Setup

**Objects in Scene:**
1. Diamond_Ring (main object, rotating)
2. Diamond_Band (gold, metallic)
3. Diamond_Stone (clear, reflective)
4. Diamond_Prongs (emissive, glowing)

### 4.2 Animation Configuration

**Diamond_Ring Rotation:**
- Frame 1: Z = 0°
- Frame 240: Z = 360°
- Interpolation: Linear

**Prongs Emissive:**
- Material: "Prongs_Emissive"
- Emission enabled
- Strength: Keyframed 0 → 1 → 0

### 4.3 Preview

1. Press Spacebar in Timeline
2. Observe:
   - Ring rotates smoothly
   - Prongs glow in sync with rotation
   - Reflections change on diamond

---

## Part 5: Nike Shoe Animation - Eyelet Glow

### 5.1 Eyelet Highlighting Animation

**Concept:** Eyelets light up sequentially as shoe rotates.

### 5.2 Material Setup

**Create Material: "Eyelet_Glow"**

```
Nodes:
1. Principled BSDF
   - Base Color: #808080 (gray metal)
   - Metallic: 1.0
   - Roughness: 0.2

2. Emission Shader
   - Color: #FF6600 (orange highlight)
   - Strength: 0.0 (initially off)

3. Mix Shader
   - Mix Factor: [Animated per eyelet]

4. Material Output
```

### 5.3 Per-Eyelet Animation (Advanced)

For multiple eyelets with staggered glow:

1. Duplicate eyelet object 5 times
2. Assign separate materials for each:
   - Eyelet_1_Glow
   - Eyelet_2_Glow
   - etc.

3. Keyframe each with offset:
   ```
   Eyelet_1: Strength 0 → 2 at frame 40 → 0 at frame 100
   Eyelet_2: Strength 0 → 2 at frame 80 → 0 at frame 140
   Eyelet_3: Strength 0 → 2 at frame 120 → 0 at frame 180
   Eyelet_4: Strength 0 → 2 at frame 160 → 0 at frame 220
   Eyelet_5: Strength 0 → 2 at frame 200 → 0 at frame 240
   ```

4. Result: Sequential eyelet glow as shoe rotates

---

## Part 6: Shader Animation with Drivers

### 6.1 Advanced: Using Drivers

For more complex animations tied to object properties:

1. Right-click property (e.g., Emission Strength)
2. "Add Driver"
3. In Driver Editor:
   - Type: Expression
   - Expression: `sin(frame / 30) * 2` (oscillating glow)
   - Frame: Use current frame

Result: Emissive strength oscillates smoothly based on timeline frame.

### 6.2 Expression Examples

```
Linear increase:
frame / 240

Sine wave (oscillating):
sin(frame / 30) * 2

Sawtooth (repeating):
(frame % 60) / 60

Bounce effect:
abs(sin(frame / 20))

Random variation:
noise(frame) * 2
```

---

## Part 7: Rendering Animation

### 7.1 Render Animation to Video

**Setup:**

1. Properties → Output Properties
2. Output Path: `//renders/animation`
3. File Format: `FFmpeg Video`
4. Container: `MPEG-4`
5. Codec: `H.264`
6. Quality: 100 (highest)

**Render:**
1. Menu: `Render` → `Render Animation`
2. Or press `Ctrl+F12`
3. Wait for completion

**Output:** Video file saved as `animation_0001.mp4`

### 7.2 Render to Image Sequence

Better for stopping/resuming:

1. Output Format: `PNG`
2. Properties:
   - Color Depth: 16-bit (for post-processing)
   - Compression: 90

3. Render: `Ctrl+F12`
4. Output: `animation_0001.png`, `animation_0002.png`, etc.

### 7.3 Post-Process (Optional)

Use VSCode Video Editor or FFmpeg:

```bash
# Combine PNG sequence into MP4
ffmpeg -framerate 24 -i animation_%04d.png -c:v libx264 -crf 23 output.mp4
```

---

## Part 8: Optimized Emissive Material for AR

### 8.1 Performance Considerations

**Mobile AR Shader (Simplified):**

```glsl
#version 330

uniform sampler2D albedoTexture;
uniform sampler2D normalTexture;
uniform float emissionStrength;
uniform vec3 emissionColor;

in vec2 uv;
in vec3 normal;

void main() {
    vec4 albedo = texture(albedoTexture, uv);
    vec3 emissive = emissionColor * emissionStrength;
    
    vec3 finalColor = albedo.rgb + emissive;
    gl_FragColor = vec4(finalColor, albedo.a);
}
```

**Optimization Tips:**
- Limit to 1-2 emissive materials per scene
- Use simple solid colors (no textures for glow)
- Reduce animation complexity (fewer keyframes)
- Bake lighting instead of computing at runtime

### 8.2 Eevee Specific Settings

For real-time preview in Blender:

1. Material Properties → Settings
2. Blend Mode: "Blend" (transparent)
3. Enable Bloom:
   - Render Properties → Bloom
   - Threshold: 0.8
   - Intensity: 0.05

Result: Emissive materials have realistic bloom effect.

---

## Part 9: Advanced Animation Examples

### Example 1: Camera Shutter Opening

**Setup:**
- Shutter blades rotate open
- Emissive interior reveals light

**Animation:**
```
Frame 1-30: Shutter closed, dark interior
Frame 30-90: Shutter opens (rotate Z: 0° → 90°)
Frame 90-120: Interior glow intensifies (emission 0 → 2)
Frame 120-180: Shutter closing
Frame 180-240: Shutter closed, no emission
```

### Example 2: Jewelry Polishing Shine

**Setup:**
- Ring rotates
- Brief emission "flash" as light hits facet

**Animation:**
```
Frame 1-60: Normal material
Frame 60-80: Emission spike (0 → 3 → 0)
Frame 80-120: Back to normal
Frame 120-180: Another rotation + flash
```

**Implementation:**
```
Emission Strength Keyframes:
Frame 60: 0
Frame 70: 3 (peak brightness)
Frame 80: 0

Graph: Sharp rise, sharp fall (V-shaped keyframe)
```

### Example 3: Heat Dissipation

**Setup:**
- Hot object cools over time
- Color changes from red to orange to dark

**Keyframe Animation:**
```
Emission Color Gradient:
Frame 1: #FF4500 (orange-red, hot)
Frame 80: #FF8C00 (orange, cooling)
Frame 160: #8B4513 (brown, nearly cool)
Frame 240: #000000 (black, fully cool)

Emission Strength:
Frame 1: 2.0
Frame 80: 1.0
Frame 160: 0.5
Frame 240: 0.0
```

---

## Part 10: Testing and Export

### 10.1 Preview in Viewport

1. Switch to Material Preview or Rendered mode
2. Press Spacebar to play animation
3. Verify:
   - Rotation smooth and continuous
   - Emission intensity correct
   - Color transitions smooth
   - No clipping or artifacts

### 10.2 Export Animation Options

**Option A: Video File (for web/presentation)**
- Format: MP4 (H.264)
- Resolution: 1920×1080 or 1280×720
- Frame rate: 24 fps

**Option B: Image Sequence (for custom processing)**
- Format: PNG 16-bit
- Resolution: 1920×1080
- Sequence: animation_0001.png - animation_0240.png

**Option C: Optimized Model with Animation**
- Format: glTF with animation tracks
- Include all material data
- Use packed textures for optimization

### 10.3 Integration with AR Platform

Export settings for AR:
```
- Format: glTF Binary (.glb)
- Include: All animations, materials
- Texture size: 2K (2048×2048)
- Animation FPS: 24 or 30
- Total model size: < 20 MB
```

---

## Deliverables Checklist

For Diamond Ring Animation:

- [ ] Rotation animation created (360° over 10 seconds)
- [ ] Emissive material assigned to prongs
- [ ] Emission strength keyframed (0 → 1 → 0)
- [ ] Animation preview in Material Preview mode
- [ ] Animation rendered to video/image sequence
- [ ] Color and intensity verified in AR context

For Nike Shoe Animation:

- [ ] Eyelet materials created with emission
- [ ] Sequential glow animation keyframed
- [ ] Shoe rotation synchronized with eyelet glow
- [ ] Animation rendered to video
- [ ] Performance optimized for mobile AR

---

## Troubleshooting

### Problem: Emissive material too bright/too dark
- **Solution**: Adjust Emission Strength value (0.5 to 5.0)
- **Solution**: Use Bloom post-processing to enhance effect

### Problem: Animation doesn't loop properly
- **Solution**: Ensure last keyframe matches first
- **Solution**: Enable Timeline cycle option (wrapping)

### Problem: Emission looks wrong in Eevee
- **Solution**: Enable Bloom in render settings
- **Solution**: Check emissive color is in correct color space

### Problem: Animation export too large
- **Solution**: Reduce texture resolution (2K instead of 4K)
- **Solution**: Remove unnecessary keyframes
- **Solution**: Use compression (H.264 for video)

---

## Next Steps

1. Create rotation animation for chosen object
2. Add emissive material to secondary object
3. Keyframe emission strength and color
4. Preview in Material Preview mode
5. Render to video file
6. Export as optimized glB with animation

