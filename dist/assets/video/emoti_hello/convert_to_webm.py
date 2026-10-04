#!/usr/bin/env python3
import subprocess
from pathlib import Path

INPUT_DIR  = Path('./mp4green')
OUTPUT_DIR = Path('./webm')

COLOR      = '0x14AF3B'
SIMILARITY = '0.11'   # ← más permisivo
BLEND      = '0.08'   # ← suaviza bordes

CROP       = 'crop=480:ih:400:0'

OUTPUT_DIR.mkdir(exist_ok=True)

for mp4_file in INPUT_DIR.glob('*.mp4'):
    print(f'Procesando {mp4_file.name} …')
    webm = OUTPUT_DIR / (mp4_file.stem + '.webm')

    subprocess.run([
        'ffmpeg', '-y', '-i', str(mp4_file),
        '-filter_complex', f'{CROP},chromakey={COLOR}:{SIMILARITY}:{BLEND},format=yuva420p',
        '-c:v', 'libvpx-vp9', '-auto-alt-ref', '0',
        '-b:v', '0', '-crf', '30', '-cpu-used', '5',
        '-row-mt', '1', '-threads', '4', '-an', str(webm)
    ], check=True)

print('Terminado – recortados y sin fondo (más permisivo) en', OUTPUT_DIR.resolve())