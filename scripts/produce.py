#!/usr/bin/env python3
"""Gera vídeos verticais com roteiro original, narração IA e ffmpeg; não publica."""
import argparse
from fractions import Fraction
import datetime as dt
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 720, 1280
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
FONT_REGULAR = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
ACCENTS = [(59,234,199), (125,154,255), (250,148,108), (231,108,213)]
DAYS = [1, 3, 5, 6]  # terça, quinta, sábado e domingo; segunda=0
HOURS = ["18:00","10:00","10:00","18:00"]

def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)

def probe(path):
    return json.loads(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries",
         "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate",
         "-of","json",str(path)], text=True))

def seconds(path):
    return float(probe(path)["format"]["duration"])

def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)

def lines_fit(draw, text, fnt, width):
    result = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        buf = ""
        for word in words:
            attempt = (buf + " " + word).strip()
            if buf and draw.textbbox((0,0), attempt, font=fnt)[2] > width:
                result.append(buf)
                buf = word
            else:
                buf = attempt
        result.append(buf)
    return result

def card(path, item, scene, index, count):
    accent=ACCENTS[index%len(ACCENTS)]
    im=Image.new("RGB",(W,H),(10,13,26))
    d=ImageDraw.Draw(im)
    for y in range(H):
        d.line((0,y,W,y),fill=(int(10+9*y/H),int(13+10*y/H),int(26+19*y/H)))
    rng=random.Random(item["id"]+str(index))
    for _ in range(50):
        x,y=rng.randrange(20,W-20),rng.randrange(100,H-100)
        d.ellipse((x-2,y-2,x+2,y+2),fill=(30,38,56))
    d.rounded_rectangle((42,82,W-42,142),radius=24,fill=(24,34,49),outline=(45,64,79),width=2)
    d.text((64,96),"METON DIGITAL | 100% IA",font=font(21,True),fill=accent)
    d.ellipse((475,178,758,460),fill=tuple(int(v*.16) for v in accent))
    d.ellipse((525,229,690,395),outline=accent,width=8)
    d.rounded_rectangle((548,262,666,363),radius=24,outline=(225,236,250),width=6)
    d.line((578,309,601,335,636,291),fill=accent,width=7)
    d.text((44,206),f"{index+1:02d} / {count:02d}",font=font(32,True),fill=accent)
    y=480
    for ln in lines_fit(d,scene["heading"].upper(),font(48,True),615)[:4]:
        d.text((46,y),ln,font=font(48,True),fill=(248,249,254))
        y+=63
    y+=24
    rule_y=min(y,H-450)
    d.rounded_rectangle((46,rule_y,W-46,rule_y+7),radius=3,fill=accent)
    y=rule_y+42
    for ln in lines_fit(d,scene["body"],font(31),614)[:11]:
        d.text((46,y),ln,font=font(31),fill=(217,224,236))
        y+=46
    d.rounded_rectangle((46,H-155,W-46,H-147),radius=4,fill=(49,58,75))
    d.rounded_rectangle((46,H-155,46+int((W-92)*(index+1)/count),H-147),radius=4,fill=accent)
    d.text((46,H-119),"DICAS ORIGINAIS  |  @metonalencar",font=font(22),fill=(167,187,205))
    d.text((46,H-78),"Conteúdo informativo. Confira fontes oficiais.",font=font(17),fill=(119,138,158))
    path.parent.mkdir(parents=True,exist_ok=True)
    im.save(path,optimize=True)

def build_scenes(item):
    start={"heading":item["title"],"body":item["hook"],
           "say":item["hook"]+" Neste vídeo, veja quatro cuidados práticos que você pode aplicar agora. São orientações educativas, sem promessas milagrosas nem necessidade de comprar aplicativos."}
    middle=[{"heading":title,"body":speech.split(". ")[0].strip().rstrip(".")+".","say":speech}
            for title,speech in item["tips"]]
    end={"heading":"SALVE E COMPARTILHE","body":item["cta"],
         "say":item["cta"]+" Acompanhe a página para mais dicas originais sobre tecnologia, privacidade e segurança digital."}
    return [start]+middle+[end]

def make_voice(text, audio_path, mode):
    # Primeiro, voz neural gratuita (quando o serviço está disponível).
    if mode in ("auto","edge") and shutil.which("edge-tts"):
        try:
            run(["edge-tts","--voice","pt-BR-AntonioNeural","--rate","-6%",
                "--text",text,"--write-media",str(audio_path)],
                stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=120)
            if audio_path.exists() and audio_path.stat().st_size>1000:
                return "edge-tts"
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
            print("Edge TTS indisponível:",exc,file=sys.stderr)
            audio_path.unlink(missing_ok=True)
    if mode=="edge":
        raise RuntimeError("Edge TTS indisponível, e fallback não autorizado")
    # Segunda opção: Google Translate TTS, sem chave de API.
    if mode=="auto":
        try:
            from gtts import gTTS
            gTTS(text=text,lang="pt",tld="com.br",slow=False,lang_check=False,timeout=15).save(str(audio_path))
            if audio_path.exists() and audio_path.stat().st_size>1000:
                return "gtts"
        except Exception as exc:
            print("gTTS indisponível:",exc,file=sys.stderr)
            audio_path.unlink(missing_ok=True)
    # Último recurso: voz local sem conexão. Pode soar robótica.
    wav=audio_path.with_suffix(".wav")
    run(["espeak","-v","pt-br","-s","152","-a","160","-w",str(wav),text],
        stdout=subprocess.DEVNULL)
    run(["ffmpeg","-y","-loglevel","error","-i",str(wav),
        "-c:a","libmp3lame","-b:a","96k",str(audio_path)])
    wav.unlink(missing_ok=True)
    return "espeak"

def generate(item, out, voice_mode, overwrite):
    out.mkdir(parents=True,exist_ok=True)
    movie=out/(item["id"]+".mp4")
    if movie.exists() and not overwrite:
        return {"name":movie.name,"duration":seconds(movie),"voice":"cache"}
    temp=out/(".working_"+item["id"])
    temp.mkdir(parents=True,exist_ok=True)
    scenes=build_scenes(item)
    spoken="\n\n".join(s["say"] for s in scenes)
    voice=make_voice(spoken,temp/"voice.mp3",voice_mode)
    duration=seconds(temp/"voice.mp3")
    weights=[max(8,len(s["say"].split())) for s in scenes]
    total=sum(weights)
    lengths=[max(3.0,duration*w/total) for w in weights]
    lengths[-1]+=max(0,duration-sum(lengths))+0.95
    # Renderização B+: mascote NEXO em movimento, cenas e legendas dinâmicas.
    # O áudio é preservado, e toda animação é gerada em Python/Pillow + ffmpeg.
    from visual_bplus import render_video
    visual=render_video(scenes,temp/"voice.mp3",movie,duration)
    info=probe(movie)
    v=[s for s in info["streams"] if s["codec_type"]=="video"]
    a=[s for s in info["streams"] if s["codec_type"]=="audio"]
    duration=float(info["format"]["duration"])
    if not (len(v)==1 and len(a)==1 and v[0]["codec_name"]=="h264"
            and Fraction(v[0]["avg_frame_rate"]) == 30
            and v[0]["width"]==720 and v[0]["height"]==1280 and duration>=61):
        raise RuntimeError(f"Arquivo inválido ou curto: {movie} ({duration:.1f}s)")
    shutil.rmtree(temp,ignore_errors=True)
    return {"name":movie.name,"duration":duration,"voice":voice,"visual_format":visual["visual_format"],"segments":visual["segments"]}

def nearest_monday(date):
    return date+dt.timedelta(days=(-date.weekday())%7)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--week-date",default=None)
    p.add_argument("--out",default=str(ROOT/"public"))
    p.add_argument("--count",type=int,default=4)
    p.add_argument("--voice",choices=["auto","edge","espeak"],default="auto")
    p.add_argument("--repo",default=os.getenv("GITHUB_REPOSITORY",""))
    p.add_argument("--overwrite",action="store_true")
    opt=p.parse_args()
    bank=json.loads((ROOT/"topics.json").read_text(encoding="utf-8"))
    assert len(bank)>=4 and len(set(x["id"] for x in bank))==len(bank)
    assert all(len(x["tips"])==4 for x in bank)
    today=dt.date.fromisoformat(opt.week_date) if opt.week_date else dt.date.today()
    monday=nearest_monday(today)
    if monday<dt.date(2026,10,12):
        raise RuntimeError("Data anterior ao início do projeto")
    iso=f"{monday.isocalendar().year}-W{monday.isocalendar().week:02d}"
    selected_index=(monday-dt.date(2026,10,12)).days//7*4
    selected=bank[selected_index:selected_index+opt.count]
    if len(selected)!=opt.count:
        raise RuntimeError("Roteiros inéditos esgotados: adicionar novas pautas originais antes de prosseguir")
    base=Path(opt.out).resolve()
    folder=base/"videos"/iso
    # Corrige também lotes antigos já enviados ao planejador.
    for old in base.glob("videos/*/*.mp4"):
        streams = probe(old)["streams"]
        video = next(s for s in streams if s["codec_type"] == "video")
        if Fraction(video["avg_frame_rate"]) == 30:
            continue
        fixed = old.with_name(old.stem + ".repair.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(old),
             "-vf", "fps=30,format=yuv420p", "-r", "30",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
             "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(fixed)])
        check = next(s for s in probe(fixed)["streams"] if s["codec_type"] == "video")
        if Fraction(check["avg_frame_rate"]) != 30:
            raise RuntimeError(f"Taxa inválida: {fixed}")
        fixed.replace(old)
        print("CORRIGIDO 30 FPS", old, flush=True)
    entries=[]
    for i,item in enumerate(selected):
        clip=generate(item,folder,opt.voice,opt.overwrite)
        day=monday+dt.timedelta(days=DAYS[i])
        date_time=day.isoformat()+"T"+HOURS[i]+":00"
        path=f"videos/{iso}/{clip['name']}"
        caption=item["hook"]+" "+item["cta"]+" #Tecnologia #DicasDigitais #SegurancaDigital #AprendaNoTikTok #InteligenciaArtificial"
        data={"id":iso+"-"+item["id"],"title":item["title"],"file":path,
              "publication_date":date_time,"timezone":"America/Fortaleza",
              "caption":caption,"ai_generated":True,"privacyOption":"PUBLIC_TO_EVERYONE",
              "duration_s":round(clip["duration"],1),"voice_engine":clip["voice"],
              "visual_format":clip.get("visual_format","anterior"),"animated_segments":clip.get("segments",0),
              "quality_review_required":True,"published":False}
        if opt.repo:
            data["media_url"]=f"https://raw.githubusercontent.com/{opt.repo}/main/public/{path}"
        entries.append(data)
        print(f"GERADO {path} ({clip['duration']:.1f}s) narração {clip['voice']}",flush=True)
    output=base/"manifest.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    manifest={"generated_on":dt.datetime.now(dt.timezone.utc).isoformat(),
              "week":iso,"week_start":monday.isoformat(),"account":"@metonalencar",
              "publisher":"Metricool via ChatGPT","auto_publish_enabled":False,
              "status":"media_pronta_sem_agendamento","videos":entries}
    output.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Manifesto pronto:",output)

if __name__=="__main__":
    main()
