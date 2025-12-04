import subprocess
import pathlib

BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"

blend_file = pathlib.Path("template_glow.blend").resolve()
script_file = pathlib.Path("script.py").resolve()

cmd = [
    BLENDER_PATH,
    "-b", str(blend_file),
    "-P", str(script_file),
]

subprocess.run(cmd, check=True)