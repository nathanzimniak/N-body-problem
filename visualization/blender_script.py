import bpy
import csv
import os
import math
import mathutils
import subprocess
import pathlib
import sys
import json

# Unpack command-line arguments passed after "--"
argv = sys.argv
argv = argv[argv.index("--") + 1:]
PATH_CSV_FILE     = argv[0]
PATH_OUTPUT_DIR   = argv[1]
BODY_SIZES        = json.loads(argv[2])
BODY_COLORS       = json.loads(argv[3])
TRAIL_LENGTH      = int(argv[4])
TRAIL_THICKNESS   = float(argv[5])
EMISSION_STRENGTH = float(argv[6])
FPS               = int(argv[7])
RES_X             = int(argv[8])
RES_Y             = int(argv[9])
FRAME_START       = int(argv[10])
FRAME_END         = int(argv[11])
CAM_LOCATION      = json.loads(argv[12])
CAM_TARGET        = json.loads(argv[13])

# Convert keys back to int (JSON keys are strings)
BODY_SIZES   = {int(k): float(v) for k, v in BODY_SIZES.items()}
BODY_COLORS  = {int(k): str(v) for k, v in BODY_COLORS.items()}
CAM_LOCATION = tuple(CAM_LOCATION)
CAM_TARGET   = tuple(CAM_TARGET)

# Number of frames per year (assuming time t is in years)
FRAMES_PER_YEAR = 365.0

# Interpolation step for trails
TRAIL_STEP_FRAMES = 0.25


# Function to convert hex color to RGBA
def hex_to_rgba(hex_color, alpha_override=1.0):
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        return (1.0, 1.0, 1.0, alpha_override)
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, alpha_override)


scene = bpy.context.scene


# Clean up existing mesh objects
for obj in list(bpy.data.objects):
    if obj.type == 'MESH':
        bpy.data.objects.remove(obj, do_unlink=True)



# Setup render settings
scene.render.engine                = 'BLENDER_EEVEE' #'CYCLES'
scene.render.resolution_x          = RES_X
scene.render.resolution_y          = RES_Y
scene.render.resolution_percentage = 100
scene.render.fps                   = FPS
scene.frame_start                  = FRAME_START
scene.frame_end                    = FRAME_END
scene.render.use_motion_blur       = False
scene.cycles.samples               = 32
scene.cycles.preview_samples       = 16

if scene.render.engine == 'CYCLES':
    cycles_settings = scene.cycles
    if hasattr(cycles_settings, "motion_blur_shutter"):
        cycles_settings.motion_blur_shutter = 0.5

# Setup black background
world = scene.world
nt    = world.node_tree
bg    = None

for node in nt.nodes:
    if node.type == 'BACKGROUND':
        bg = node
        break

if bg: bg.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)

# Setup camera
for obj in list(bpy.data.objects):
    if obj.type == 'CAMERA':
        bpy.data.objects.remove(obj, do_unlink=True)

cam_data = bpy.data.cameras.new("Camera")
cam_obj  = bpy.data.objects.new("Camera", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = CAM_LOCATION

def look_at(obj, target):
    target_vec = mathutils.Vector(target)
    direction = target_vec - obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

look_at(cam_obj, CAM_TARGET)


# Setup material with emission shader
def make_material_for_body(body_id: int, hex_color: str):
    rgba = hex_to_rgba(hex_color)
    mat = bpy.data.materials.new(name=f"GlowMaterial_{body_id}")
    mat.use_nodes = True

    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    for n in list(nodes):
        nodes.remove(n)

    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = rgba
    emission.inputs["Strength"].default_value = EMISSION_STRENGTH
    output = nodes.new("ShaderNodeOutputMaterial")
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat


# Import data from CSV and create animated objects
objects                 = {}
cleared_bodies          = set()
positions_by_body_frame = {}
body_materials          = {}

with open(PATH_CSV_FILE, newline='') as f:
    reader = csv.DictReader(f)

    for row in reader:
        t = float(row["t"])
        body_id = int(row["body"])
        x, y, z = float(row["x"]), float(row["y"]), float(row["z"])

        frame = int(round(t * FRAMES_PER_YEAR))
        if frame < FRAME_START or frame > FRAME_END:
            continue

        if body_id not in positions_by_body_frame:
            positions_by_body_frame[body_id] = {}
        positions_by_body_frame[body_id][frame] = (x, y, z)

        obj_name = f"body_{body_id}"

        if body_id not in objects:
            radius = BODY_SIZES[body_id]
            bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(x, y, z))
            obj = bpy.context.view_layer.objects.active
            if obj is None:
                raise RuntimeError("Impossible de récupérer la sphère nouvellement créée.")
            obj.name = obj_name

            hex_color = BODY_COLORS.get(body_id, "#ffffff")
            mat = make_material_for_body(body_id, hex_color)
            obj.data.materials.append(mat)
            body_materials[body_id] = mat

            objects[body_id] = obj
        else:
            obj = objects[body_id]

        if body_id not in cleared_bodies:
            obj.animation_data_clear()
            cleared_bodies.add(body_id)

        obj.location = (x, y, z)
        obj.keyframe_insert("location", frame=frame)

# Create trail objects
trail_objects = {}

for body_id, main_obj in objects.items():
    ghosts = []
    base_radius = BODY_SIZES[body_id] * TRAIL_THICKNESS
    mat = body_materials.get(body_id, None)

    for k in range(TRAIL_LENGTH):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=base_radius, location=main_obj.location)
        ghost = bpy.context.view_layer.objects.active
        ghost.name = f"body_{body_id}_trail_{k}"

        if mat is not None: ghost.data.materials.append(mat)

        ghost.hide_render = True
        ghost.hide_viewport = True

        ghosts.append(ghost)

    trail_objects[body_id] = ghosts

# Animate trail objects
for body_id, frames_dict in positions_by_body_frame.items():
    ghosts = trail_objects.get(body_id, [])
    if not ghosts: continue

    for frame in range(FRAME_START, FRAME_END + 1):
        if frame not in frames_dict:
            for ghost in ghosts:
                ghost.hide_render = True
                ghost.hide_viewport = True
                ghost.keyframe_insert("hide_render", frame=frame)
                ghost.keyframe_insert("hide_viewport", frame=frame)
            continue

        for k, ghost in enumerate(ghosts):
            source_time = frame - k * TRAIL_STEP_FRAMES

            if source_time < FRAME_START:
                ghost.hide_render = True
                ghost.hide_viewport = True
                ghost.keyframe_insert("hide_render", frame=frame)
                ghost.keyframe_insert("hide_viewport", frame=frame)
                continue

            f0 = int(math.floor(source_time))
            f1 = int(math.ceil(source_time))

            if f0 not in frames_dict or f1 not in frames_dict:
                ghost.hide_render = True
                ghost.hide_viewport = True
                ghost.keyframe_insert("hide_render", frame=frame)
                ghost.keyframe_insert("hide_viewport", frame=frame)
                continue

            if f0 == f1:
                v = mathutils.Vector(frames_dict[f0])
            else:
                t = source_time - f0  # entre 0 et 1
                v0 = mathutils.Vector(frames_dict[f0])
                v1 = mathutils.Vector(frames_dict[f1])
                v = v0.lerp(v1, t)

            ghost.location = v

            scale_factor = max(0.2, 1.0 - (k / TRAIL_LENGTH))
            ghost.scale = (scale_factor, scale_factor, scale_factor)

            ghost.hide_render = False
            ghost.hide_viewport = False
            ghost.keyframe_insert("hide_render", frame=frame)
            ghost.keyframe_insert("hide_viewport", frame=frame)
            ghost.keyframe_insert("location", frame=frame)
            ghost.keyframe_insert("scale", frame=frame)


# Setup output settings
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode  = 'RGB'
scene.render.image_settings.color_depth = '8'
scene.render.filepath = os.path.join(PATH_OUTPUT_DIR, "frame_")

# Render the animation
bpy.ops.render.render(animation=True)