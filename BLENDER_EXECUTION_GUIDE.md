# 🎬 BLENDER EXECUTION GUIDE

**This project runs entirely in Blender 3.4+**

---

## ✅ PREREQUISITES

### Required
- ✅ **Blender 3.4+** installed
- ✅ **3 GLB models downloaded** from Sketchfab
- ✅ **HDRI files downloaded** from Polyhaven

### Optional
- Substance Painter (for texture refinement)
- Photoshop (for image editing)

---

## 🚀 EXECUTION WORKFLOW

### **Phase 1: Scene Setup in Blender (1 hour)**

#### Step 1.1: Launch Blender
```
Launch Blender → Start with "General" project
```

#### Step 1.2: Configure World Settings
1. Go to **Shading** workspace (top menu)
2. Toggle to **World** mode (small sphere icon)
3. Add **Background** shader
4. Load HDRI:
   - Add **Image Texture** node
   - Click "Open" → Select `studio.exr` or `urban.exr`
   - Connect to **Background** shader
5. Set brightness:
   - **Background Strength**: 2.0

#### Step 1.3: Add Lighting
1. Add **Sun Lamp**: `Shift+A` → Light → Sun
   - Rotation: X=45°, Z=45°
   - Energy: 2.0

#### Step 1.4: Configure Render Settings
1. Render engine: **Eevee** (real-time)
2. Resolution: 1920×1440
3. Frame rate: 24 fps
4. Output path: `//renders/`

---

### **Phase 2: Import & Apply Materials (6-8 hours)**

#### For EACH Model (Ring, Earring, Shoe):

**Step 2.1: Import Model**
```
File → Import → glTF 2.0 (.glb/.gltf)
Select: [model].glb
```

**Step 2.2: Switch to Shading Workspace**
- Top menu → **Shading**
- Enable **Material Preview** viewport shading

**Step 2.3: Create PBR Materials**
Follow `BLENDER_WORKFLOW.md` Part 3-6

Materials to create:
- Gold_Polished (jewelry)
- Diamond_Clear (jewelry)
- Metal_Brushed (prongs/eyelets)
- Rubber_Black (shoe sole)
- Fabric_Weave (shoe mesh)
- Leather_Synthetic (shoe panels)

**Step 2.4: Material Node Setup**
For each material:
1. Add **Principled BSDF** (if not present)
2. Set **Base Color** (Albedo)
3. Add **Roughness** texture (Noise → ColorRamp)
4. Set **Metallic** value (0 or 1)
5. Create **Normal Map** (Noise → Bump → Normal)

**Step 2.5: Assign Materials to Objects**
1. Select mesh object
2. Material Properties (right panel)
3. Select material slot
4. Click "Assign"

**Step 2.6: Test in Viewport**
- Switch to **Material Preview** mode
- Verify reflections and detail
- Adjust if needed

---

### **Phase 3: Optimization (2-3 hours)**

#### Step 3.1: Texture Packing
Follow `TEXTURE_PACKING_GUIDE.md`

1. Create individual texture maps
2. Combine Roughness + Metallic into single RGBA texture
3. Result: 42% memory savings

#### Step 3.2: Shader Optimization
- Keep nodes < 25 per material
- Remove unused nodes
- Verify real-time performance

---

### **Phase 4: Animation & Emissive (2-4 hours)**

#### Step 4.1: Add Rotation Animation
1. Switch to **Animation** workspace
2. Select object (e.g., Diamond Ring)
3. Set Timeline:
   - Start: Frame 1
   - End: Frame 240 (10 seconds at 24 fps)

#### Step 4.2: Create Keyframes
```
Frame 1:   Insert Rotation → Z = 0°
Frame 120: Insert Rotation → Z = 180°
Frame 240: Insert Rotation → Z = 360°
```

#### Step 4.3: Add Emissive Material
1. Create new material: "Prongs_Emissive"
2. Add **Emission** shader
3. Create **Mix Shader** (blend base + emission)
4. Keyframe emission strength:
   - Frame 1: 0 (no glow)
   - Frame 120: 2 (peak glow)
   - Frame 240: 0 (no glow)

#### Step 4.4: Enable Bloom Effect
Render Properties → **Bloom**:
- Intensity: 0.05
- Threshold: 0.8

#### Step 4.5: Preview Animation
- Press **Spacebar** in Timeline to play
- Verify smooth rotation and glow

---

### **Phase 5: Export (1-2 hours)**

#### Step 5.1: Export Models with Materials
```
File → Export → glTF 2.0 (.glb/.gltf)
Settings:
  ✅ Include Materials
  ✅ Include Animations (if applicable)
  ✅ Bake Animation
Output: blender/[model]_pbr.glb
```

#### Step 5.2: Export Animation to Video
```
Render Properties → Output
Format: FFmpeg Video (MP4)
Codec: H.264
Render: Ctrl+F12 (render animation)
Output: renders/animation.mp4
```

#### Step 5.3: Verify Exports
- Check file sizes (< 20 MB each)
- Open in glTF viewer to validate
- Ensure no missing textures

---

## 📋 STEP-BY-STEP CHECKLIST

### **Ring Project (blender/diamond_ring.blend)**

- [ ] **Setup Phase (Week 1)**
  - [ ] Import diamond-ring.glb
  - [ ] Add HDRI world environment
  - [ ] Add lighting
  - [ ] Configure camera

- [ ] **Materials Phase (Week 2)**
  - [ ] Create Gold_Polished material
  - [ ] Create Diamond_Clear material
  - [ ] Create Metal_Brushed material
  - [ ] Assign to all objects
  - [ ] Test in Material Preview

- [ ] **Optimization Phase (Week 3)**
  - [ ] Create packed textures
  - [ ] Verify performance > 60 FPS

- [ ] **Animation Phase (Week 4)**
  - [ ] Add rotation keyframes (360°)
  - [ ] Create Prongs_Emissive material
  - [ ] Keyframe emission (0→2→0)
  - [ ] Enable Bloom effect
  - [ ] Preview animation

- [ ] **Export Phase (Week 4)**
  - [ ] Export to diamond_ring_pbr.glb
  - [ ] Export animation to MP4
  - [ ] Verify in glTF viewer

---

### **Earring Project (blender/earring.blend)**

- [ ] Import earring.glb
- [ ] Reuse Gold_Polished material
- [ ] Reuse Diamond_Clear material
- [ ] Assign to objects
- [ ] Test materials
- [ ] Export to earring_pbr.glb

---

### **Nike Shoe Project (blender/nike_shoe.blend)**

- [ ] Import nike-shoe.glb
- [ ] Create Rubber_Black material
- [ ] Create Fabric_Weave material
- [ ] Create Metal_Brushed material (reuse)
- [ ] Create Leather_Synthetic material
- [ ] Assign all materials
- [ ] Test in viewport
- [ ] Optional: Add sequential eyelet glow animation
- [ ] Export to nike_shoe_pbr.glb

---

## 🎨 QUICK MATERIAL NODE GRAPHS

### Gold_Polished
```
Noise (scale 15) → ColorRamp → Roughness
1.0 (value) → Metallic
Noise (scale 50) → Bump → Normal
#D4A574 (albedo) → Base Color
All → Principled BSDF → Output
```

### Diamond_Clear
```
#FFFACD → Base Color
0.05 → Roughness
0.0 → Metallic
1.5 → IOR
All → Principled BSDF → Output
```

### Rubber_Black
```
#1A1A1A → Base Color
Noise (scale 30) → ColorRamp → Roughness
0.0 → Metallic
Wave (scale 100) + Noise → Bump → Normal
All → Principled BSDF → Output
```

---

## 🎬 TIMELINE COMMANDS

### Essential Keyboard Shortcuts
```
Spacebar        → Play/Pause animation
I               → Insert Keyframe
R               → Rotate (then X/Y/Z for axis)
G               → Grab/Move
S               → Scale
X               → Delete
Tab             → Edit mode
F12             → Render single frame
Ctrl+F12        → Render animation
```

---

## 🔍 RENDER SETTINGS FOR AR

### Eevee (Real-Time Engine)
```
Ambient Occlusion: Enable
Bloom: Enable (intensity 0.05)
SSAO: Enable
Depth of Field: Optional
Motion Blur: Optional
```

### Cycles (Offline Quality)
```
Samples: 256 (high quality)
Denoise: Enable
Render Time: 30-60 seconds per frame
Output: PNG 16-bit for best quality
```

---

## 🚨 COMMON ISSUES & FIXES

### Problem: Materials look too dark
- **Fix**: Increase HDRI brightness to 2.5-3.0
- **Fix**: Add sun lamp with energy 2.0+

### Problem: Metallic surfaces don't reflect
- **Fix**: Verify Metallic = 1.0 in Principled BSDF
- **Fix**: Switch to Material Preview viewport mode

### Problem: Animation doesn't play
- **Fix**: Ensure keyframes are in Timeline
- **Fix**: Check End Frame is set > current frame

### Problem: File too large
- **Fix**: Reduce texture resolution (4K → 2K)
- **Fix**: Use packed textures instead of individual maps

### Problem: Emissive material not visible
- **Fix**: Enable Bloom in Render Properties
- **Fix**: Increase Emission Strength (2.0-5.0)
- **Fix**: Use Rendered viewport mode

---

## 📊 PERFORMANCE TARGETS

| Metric | Target | Check |
|--------|--------|-------|
| FPS (Eevee) | > 60 | Play in viewport |
| Shader Nodes | < 25 per material | Blender Info panel |
| File Size | < 20 MB per model | Check file properties |
| Render Time | < 5ms (Eevee) | Performance monitor |
| Memory | < 50 MB total | Project size |

---

## 🎯 DAILY EXECUTION SCHEDULE

### **Day 1-2: Setup (4-5 hours)**
1. Launch Blender
2. Configure World/HDRI
3. Add lighting
4. Configure render settings
5. Import first model

### **Day 3-4: Materials (4-6 hours)**
1. Create PBR materials for ring
2. Assign to objects
3. Test in Material Preview
4. Refine properties

### **Day 5-6: More Materials (4-6 hours)**
1. Create shoe materials
2. Complete material assignments
3. Verify all materials look correct

### **Day 7: Optimization (2-3 hours)**
1. Create packed textures
2. Verify performance
3. Optimize shader nodes

### **Day 8: Animation (2-3 hours)**
1. Add rotation keyframes
2. Create emissive material
3. Keyframe emission
4. Test animation playback

### **Day 9: Export (1-2 hours)**
1. Export all models (.glb)
2. Render animation to video
3. Verify exports
4. Validate in glTF viewer

---

## ✅ SUCCESS CRITERIA

Your Blender project is complete when:

✅ All 3 models have complete PBR materials  
✅ Materials look photorealistic in Material Preview  
✅ HDRI reflections visible on metallic surfaces  
✅ Animation plays smoothly (no stuttering)  
✅ Emissive material glows correctly  
✅ All models export to .glb format  
✅ File sizes < 50 MB total  
✅ Performance > 60 FPS in viewport  

---

## 📚 REFERENCE DOCUMENTS

Use these alongside this guide:

1. **MATERIAL_ANALYSIS.md** - Material properties & strategy
2. **BLENDER_WORKFLOW.md** - Complete detailed guide (10 parts)
3. **TEXTURE_PACKING_GUIDE.md** - Optimization details
4. **ANIMATION_AND_EMISSIVE.md** - Animation specifics
5. **FINAL_REPORT_TEMPLATE.md** - Document your work

---

## 🚀 READY TO START

Everything is set up in Blender. Follow this guide day-by-day and you'll have production-ready PBR materials in 9 days (or faster).

**Open Blender and begin with Phase 1!**

