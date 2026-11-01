#!/usr/bin/env python3
"""Renderizador do piloto Blender. SEM PUBLICAÇÃO, SEM AGENDAMENTO."""
import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"public"/"pilotos"
OUT.mkdir(parents=True,exist_ok=True)
SCRATCH=ROOT/".pilot_3d_tmp"
SCRATCH.mkdir(exist_ok=True)
spoken=("Você confiaria nessa rede Wi-Fi? "
        "Olha o nome de duas redes quase iguais. Uma pode ser falsa. "
        "Antes de conectar, confirme com o atendente qual é a rede oficial. "
        "E nunca ignore avisos de segurança do celular.")
audio=SCRATCH/"voz.mp3"
voice="edge-tts"
try:
 subprocess.run(["edge-tts","--voice","pt-BR-FranciscaNeural",
   "--rate=-6%","--text",spoken,"--write-media",str(audio)],
   check=True,timeout=90,capture_output=True)
except Exception as exc:
 voice="espeak"
 print("Voz neural não disponível; teste de movimento terá voz provisória:",exc,flush=True)
 wav=SCRATCH/"voz.wav"
 subprocess.run(["espeak","-v","pt-br","-s","159","-w",str(wav),spoken],check=True)
 subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(wav),
                 "-c:a","libmp3lame","-b:a","96k",str(audio)],check=True)
if not audio.exists() or audio.stat().st_size<1000:
 raise RuntimeError("Narração não foi produzida")
def probe(path):
 return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
  "format=duration:stream=width,height,avg_frame_rate,codec_type,codec_name",
  "-of","json",str(path)],text=True))
duration=max(8,float(probe(audio)["format"]["duration"])+.5)
print("Voz:",voice,"duração:",duration,flush=True)
frames=SCRATCH/"frames"
frames.mkdir(exist_ok=True)
subprocess.run(["blender","-b","-t","2","-P",str(ROOT/"scripts"/"blender_piloto.py"),
 "--",str(frames),str(duration)],check=True)
video=OUT/"piloto-3d-blender-animado.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","12",
 "-i",str(frames/"frame_%04d.png"),"-i",str(audio),
 "-vf","fps=30,scale=720:1280:flags=lanczos,format=yuv420p",
 "-c:v","libx264","-preset","veryfast","-crf","24",
 "-c:a","aac","-b:a","128k","-movflags","+faststart",
 "-t",str(duration),str(video)],check=True)
p=probe(video)
v=next(x for x in p["streams"] if x["codec_type"]=="video")
a=next(x for x in p["streams"] if x["codec_type"]=="audio")
if not (v["width"]==720 and v["height"]==1280 and v["codec_name"]=="h264" and a["codec_name"]=="aac"):
 raise RuntimeError("MP4 não passou validação técnica")
first=frames/"frame_0001.png"
last=frames/f"frame_{int(duration*12):04d}.png"
if not (first.exists() and last.exists() and first.read_bytes()!=last.read_bytes()):
 raise RuntimeError("Falha: animação não alterou visualmente os frames")
info={"title":"Teste Wi-Fi: personagem 3D real (Blender)",
 "account":"@metonalencar","duration_s":round(float(p["format"]["duration"]),1),
 "voice_engine":voice,"render_engine":"Blender Workbench 3D CPU","geometry_3d":True,
 "movement_3d":True,"approved":False,"published":False,
 "format":"720x1280 H264 AAC 30fps",
 "quality_note":"Geometria 3D procedural simplificada: não corresponde ainda ao acabamento cinematográfico da referência enviada; avaliar rosto, gestos e ações.",
 "instructions":"Não publicar nem agendar. É apenas teste de viabilidade."}
(OUT/"piloto-3d-blender-animado.json").write_text(json.dumps(info,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
print("RENDER_3D_TEST_SUCCEEDED",video,video.stat().st_size,info,flush=True)
