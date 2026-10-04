#!/usr/bin/env python3
import subprocess
from pathlib import Path
import numpy as np
from collections import Counter

INPUT_DIR  = Path('./mp4green')
OUTPUT_DIR = Path('./webm')
OUTPUT_DIR.mkdir(exist_ok=True)

def probe_size(video: Path) -> tuple[int, int]:
    """Devuelve (width, height) del vídeo."""
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'csv=p=0', str(video)
    ]
    w, h = map(int, subprocess.check_output(cmd).decode().strip().split(','))
    return w, h

def dominant_edge_color(video: Path) -> str:
    """
    Devuelve el color RGB más frecuente en la franja de 10 px superiores
    del primer frame (raw RGB24).
    """
    w_full, h_full = probe_size(video)

    # solo 10 px de alto, y reducimos anchura para ir rápido
    crop_w, crop_h = w_full // 4, 10
    cmd = [
        'ffmpeg', '-i', str(video),
        '-vf', f'crop={crop_w}:{crop_h}:0:0,scale={crop_w}:{crop_h}',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24',
        '-frames', '1', '-'
    ]
    raw = subprocess.check_output(cmd)

    frame = np.frombuffer(raw, dtype=np.uint8).reshape((crop_h, crop_w, 3))
    pixels = [tuple(px) for row in frame for px in row]
    (r, g, b), _ = Counter(pixels).most_common(1)[0]
    return f'0x{r:02X}{g:02X}{b:02X}'


for mp4_file in INPUT_DIR.glob('*.mp4'):
    print(f'Analizando color de fondo en {mp4_file.name} …')
    color = dominant_edge_color(mp4_file)
    print(f'  Color detectado: {color}')

    webm = OUTPUT_DIR / (mp4_file.stem + '.webm')
    subprocess.run([
        'ffmpeg', '-y', '-i', str(mp4_file),
        '-filter_complex', f'chromakey={color}:0.10:0.02,format=yuva420p',
        '-c:v', 'libvpx-vp9', '-auto-alt-ref', '0',
        '-b:v', '0', '-crf', '30', '-cpu-used', '5',
        '-row-mt', '1', '-threads', '4', '-an', str(webm)
    ], check=True)

print('Terminado – webms con color auto-detectado en', OUTPUT_DIR.resolve())