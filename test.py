import bpy
import csv
import sys
import os

# -----------------------------
# RÉCUPÉRATION DU CHEMIN DU CSV
# -----------------------------
argv = sys.argv
if "--" not in argv:
    raise RuntimeError("Usage : blender -b -P nbody_glow.py -- input.csv output.mp4")

argv = argv[argv.index("--") + 1:]
csv_path = argv[0]
output_path = argv[1]

print("Lecture du CSV :", csv_path)

# -----------------------------
# LECTURE DU CSV
# -----------------------------
data = []
with open(csv_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append((float(row["t"]), int(row["body"]),
                     float(row["x"]), float(row["y"]), float(row["z"])))

times = sorted({t for t, *_ in data})
time_to_frame = {t: i+1 for i, t in enumerate(times)}
N_frames = len(times)
N_bodies = max(body for (_, body, *_ ) in data) + 1

print("Nombre de corps :", N_bodies)
print("Nombre de frames :", N_frames)

# -----------------------------
# SCÈNE VIDE
# -----------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = N_frames

scene.render.engine = "BLENDER_EEVEE"
scene.render.fps = 60

# fond noir
bpy.data.worlds["World"].use_nodes = True
wn = bpy.data.worlds["World"].node_tree.nodes
wn["Background"].inputs[0].default_value = (0,0,0,1)
wn["Background"].inputs[1].default_value = 0.0

# -----------------------------
# COULEURS
# -----------------------------
def hex_to_rgba(h):
    h = h.lstrip("#")
    return (int(h[:2],16)/255, int(h[2:4],16)/255,
            int(h[4:6],16)/255, 1)

point_colors = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
colors = [hex_to_rgba(c) for c in point_colors]

# -----------------------------
# SHADER GLOW PROPRE
# -----------------------------
def make_glow_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for n in list(nodes):
        nodes.remove(n)

    # Node setup
    out = nodes.new("ShaderNodeOutputMaterial")
    mix = nodes.new("ShaderNodeMixShader")
    trans = nodes.new("ShaderNodeBsdfTransparent")
    emis = nodes.new("ShaderNodeEmission")
    layer = nodes.new("ShaderNodeLayerWeight")
    ramp = nodes.new("ShaderNodeValToRGB")

    # parameters
    emis.inputs["Color"].default_value = color
    emis.inputs["Strength"].default_value = 30.0

    layer.inputs["Blend"].default_value = 0.3  # halo largeur

    # Color ramp : centre = opaque, bord = transparent
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (1,1,1,1)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (1,1,1,0)

    # links
    links.new(layer.outputs["Facing"], ramp.inputs["Fac"])
    links.new(trans.outputs["BSDF"], mix.inputs[1])
    links.new(emis.outputs["Emission"], mix.inputs[2])
    links.new(ramp.outputs["Color"], mix.inputs["Fac"])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])

    mat.blend_method = "BLEND"
    mat.shadow_method = "NONE"
    return mat

# -----------------------------
# CRÉATION DES OBJETS
# -----------------------------
objs = {}
radius = 0.1

for i in range(N_bodies):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius)
    o = bpy.context.active_object
    o.name = f"Body_{i}"
    mat = make_glow_material(f"Glow_{i}", colors[i % len(colors)])
    o.data.materials.append(mat)
    objs[i] = o

# -----------------------------
# KEYFRAMES
# -----------------------------
for t, body, x, y, z in data:
    scene.frame_set(time_to_frame[t])
    obj = objs[body]
    obj.location = (x, y, z)
    obj.keyframe_insert("location")

# -----------------------------
# CAMÉRA
# -----------------------------
bpy.ops.object.camera_add(location=(4,-4,2))
cam = bpy.context.object
scene.camera = cam
target = bpy.data.objects.new("Target", None)
scene.collection.objects.link(target)
target.location = (0,0,0)
c = cam.constraints.new("TRACK_TO")
c.target = target
c.track_axis = "TRACK_NEGATIVE_Z"
c.up_axis = "UP_Y"

# -----------------------------
# RENDU
# -----------------------------
path = os.path.abspath(output_path)
base,_ = os.path.splitext(path)
os.makedirs(os.path.dirname(base), exist_ok=True)
scene.render.filepath = base + "_"
scene.render.image_settings.file_format = "PNG"

print("Rendu…")
bpy.ops.render.render(animation=True)
