import subprocess
import os
import json
import time

t0 = time.time()

# Preset selection
preset = "three_body_orbits"

# Paths configuration
PATH_BLENDER               = "/Applications/Blender.app/Contents/MacOS/Blender"
PATH_BLENDER_TEMPLATE_FILE = "/Users/nathanzimniak/Documents/Projets/N-body-problem/visualization/blender_template_glow.blend"
PATH_BLENDER_SCRIPT_FILE   = "/Users/nathanzimniak/Documents/Projets/N-body-problem/visualization/blender_script.py"
PATH_CSV_FILE              = rf"/Users/nathanzimniak/Documents/Projets/N-body-problem/outputs/{preset}.csv"
PATH_OUTPUT_DIR            = rf"/Users/nathanzimniak/Documents/Projets/N-body-problem/visualization/{preset}_frames"

#Style settings
if preset == "inner_solar_system":
    BODY_SIZES        = {0: 0.1, 1: 0.015, 2: 0.025, 3: 0.03, 4: 0.02}
    BODY_COLORS       = {0: "#FFB81F", 1: "#404040", 2: "#FF7B00", 3: "#0044FF", 4: "#FF2F00"}
    TRAIL_LENGTH      = 200
    TRAIL_THICKNESS   = 0.3
    EMISSION_STRENGTH = 15.0
elif preset == "three_body_orbits":
    BODY_SIZES        = {0: 0.07, 1: 0.07, 2: 0.07}
    BODY_COLORS       = {0: "#FFB81F", 1: "#006FFF", 2: "#FF2F00"}
    TRAIL_LENGTH      = 400
    TRAIL_THICKNESS   = 0.5
    EMISSION_STRENGTH = 10.0

# Visualization settings
FPS          = 60
RES_X        = 1000
RES_Y        = 1000
FRAME_START  = 1
FRAME_END    = int((sum(1 for _ in open(PATH_CSV_FILE)) - 1) / len(BODY_SIZES))
CAM_LOCATION = (0.0, -5.0, 2.0)
CAM_TARGET   = (0.0, 0.0, 0.0)

# Ensure output directory exists
os.makedirs(PATH_OUTPUT_DIR, exist_ok=True)

# Convert BODY_SIZES and BODY_COLORS to JSON strings to pass as command-line arguments
body_sizes_json   = json.dumps(BODY_SIZES)
body_colors_json  = json.dumps(BODY_COLORS)
cam_location_json = json.dumps(CAM_LOCATION)
cam_target_json   = json.dumps(CAM_TARGET)

# Launch Blender in background mode with the specified blend file and script to render frames
print("Launching Blender to render frames...\n")

cmd = [PATH_BLENDER,
       "-b", PATH_BLENDER_TEMPLATE_FILE,
       "-P", PATH_BLENDER_SCRIPT_FILE,
       "--", 
       PATH_CSV_FILE,
       PATH_OUTPUT_DIR,
       body_sizes_json,
       body_colors_json,
       str(TRAIL_LENGTH),
       str(TRAIL_THICKNESS),
       str(EMISSION_STRENGTH),
       str(FPS),
       str(RES_X),
       str(RES_Y),
       str(FRAME_START),
       str(FRAME_END),
       cam_location_json,
       cam_target_json]

subprocess.run(cmd, check=True)

print("\nRendering completed.\n")

# After rendering frames, create a video using ffmpeg
print("Creating final video with ffmpeg...\n")

os.chdir(PATH_OUTPUT_DIR)

cmd_ffmpeg = ["ffmpeg",
              "-framerate", "60",
              "-i", "frame_%04d.png",
              "-c:v", "libx264",
              "-pix_fmt", "yuv420p",
              "-crf", "18",
              "animation.mp4"]

subprocess.run(cmd_ffmpeg, check=True)

# Create GIF (simple)
cmd_ffmpeg_gif = ["ffmpeg",
                  "-framerate", "30",   # 30 fps recommandé pour les GIF
                  "-i", "frame_%04d.png",
                  "-vf", "scale=800:-1",  # optionnel: resize
                  "animation.gif"]

subprocess.run(cmd_ffmpeg_gif, check=True)

print("\nVideo creation completed.\n")

t1 = time.time()
total_time = t1 - t0

print(f"Total time : {total_time:.2f} s")