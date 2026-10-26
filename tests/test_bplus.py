"""Teste de renderização B+ independente dos posts já agendados."""
from pathlib import Path
import json, subprocess, tempfile
from fractions import Fraction
from scripts.visual_bplus import render_video
root=Path(__file__).resolve().parents[1]
bank=json.loads((root/"topics.json").read_text(encoding="utf-8"))
topic=bank[0]
scenes=[
 {"heading":topic["title"],"say":topic["hook"]},
 {"heading":topic["tips"][0][0],"say":topic["tips"][0][1]},
 {"heading":"Salve esta dica","say":topic["cta"]},
]
with tempfile.TemporaryDirectory() as t:
 folder=Path(t)
 wav=folder/"voice.wav"
 text=" ".join(s["say"] for s in scenes)
 subprocess.run(["espeak","-v","pt-br","-s","155","-w",str(wav),text],check=True)
 info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(wav)]))
 duration=float(info["format"]["duration"])
 movie=folder/"teste.mp4"
 visual=render_video(scenes,wav,movie,duration)
 info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate","-of","json",str(movie)]))
 vids=[x for x in info["streams"] if x["codec_type"]=="video"]
 auds=[x for x in info["streams"] if x["codec_type"]=="audio"]
 assert len(vids)==1 and len(auds)==1
 assert vids[0]["width"]==720 and vids[0]["height"]==1280
 assert vids[0]["codec_name"]=="h264" and Fraction(vids[0]["avg_frame_rate"])==30
 assert float(info["format"]["duration"])>=8
 assert visual["segments"]>=4
 print("B+ OK",visual,"duration",info["format"]["duration"],"bytes",movie.stat().st_size)
