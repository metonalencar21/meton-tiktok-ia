"""Renderizador B+ com NEXO, mascote digital animada, sem serviços pagos."""
from PIL import Image, ImageDraw, ImageFont
from fractions import Fraction
import bisect
import math
from pathlib import Path
import re
import subprocess

W,H,FPS=432,768,10
PINK=(252,55,142)
CYAN=(55,238,221)
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fnt(px,bold=False):
    return ImageFont.truetype(BOLD if bold else REG,px)

def box(draw,coords,radius,fill,outline=None,width=1):
    draw.rounded_rectangle(coords,radius=radius,fill=fill,outline=outline,width=width)

def wrapped(draw,string,font,max_width):
    lines=[]
    current=""
    for word in string.split():
        new=(current+" "+word).strip()
        if current and draw.textbbox((0,0),new,font=font)[2]>max_width:
            lines.append(current)
            current=word
        else:
            current=new
    if current:
        lines.append(current)
    return lines

def segments(scenes,duration):
    chunks=[]
    for scene in scenes:
        parts=[x.strip() for x in re.split(r"(?<=[.!?])\s+",scene["say"]) if x.strip()]
        for part in parts:
            chunks.append({"heading":scene["heading"],"subtitle":part})
    weights=[max(5,len(c["subtitle"].split())) for c in chunks]
    total=sum(weights)
    lengths=[duration*w/total for w in weights]
    times=[0.]
    for length in lengths:
        times.append(times[-1]+length)
    return chunks,times

def mascot(im,t,x=152,y=434,scale=0.89):
    d=ImageDraw.Draw(im)
    y+=int(4*math.sin(t*3))
    radius=int(87*scale)
    d.ellipse((x-radius-17,y-radius-16,x+radius+17,y+radius+16),fill=(20,37,64),outline=CYAN,width=2)
    d.line((x,y-radius,x,y-radius-23),fill=(134,153,187),width=5)
    d.ellipse((x-10,y-radius-37,x+10,y-radius-17),fill=PINK)
    box(d,(x-78,y+radius-3,x+78,y+radius+86),21,(42,53,93),(99,117,169),2)
    d.polygon([(x-15,y+radius+17),(x,y+radius+32),(x+15,y+radius+17)],fill=PINK)
    box(d,(x-radius-18,y-28,x-radius+7,y+34),9,(54,70,117),CYAN,2)
    box(d,(x+radius-7,y-28,x+radius+18,y+34),9,(54,70,117),CYAN,2)
    box(d,(x-radius,y-radius,x+radius,y+radius),28,(58,70,124),(139,158,214),4)
    box(d,(x-radius+14,y-radius+21,x+radius-14,y+radius-12),21,(13,20,45),(59,100,133),2)
    blink=math.sin(t*1.1)**2>0.995
    for off in (-36,36):
        if blink:
            d.line((x+off-16,y-14,x+off+16,y-14),fill=CYAN,width=4)
        else:
            d.ellipse((x+off-17,y-37,x+off+17,y+5),fill=CYAN)
            d.ellipse((x+off-5,y-25,x+off+5,y-11),fill="white")
    mouth_height=7+int(14*abs(math.sin(t*10.8)))
    box(d,(x-28,y+23,x+28,y+23+mouth_height),8,PINK)
    d.line((x-17,y+28,x+17,y+28),fill="white",width=2)
    return im

def scene_icon(draw,scene,t):
    x,y=330,342
    box(draw,(x-76,y-76,x+76,y+76),25,(32,46,79),CYAN,3)
    s=(scene["heading"]+" "+scene["subtitle"]).lower()
    if any(k in s for k in ("senha","acesso","proteja","seguran","código","dados","privac")):
        draw.arc((x-31,y-46,x+31,y+27),185,355,fill=CYAN,width=8)
        box(draw,(x-35,y-4,x+35,y+44),11,PINK)
        draw.ellipse((x-5,y+13,x+5,y+23),fill=(12,16,35))
    elif any(k in s for k in ("celular","telefone","ligue","mensag","app","tela","link","qr","whats")):
        box(draw,(x-37,y-59,x+37,y+62),12,(11,20,45),(226,234,251),4)
        box(draw,(x-24,y-31,x+24,y-10),4,(69,95,150))
        box(draw,(x-24,y+0,x+24,y+36),4,PINK)
        draw.line((x-11,y+49,x+11,y+49),fill=CYAN,width=3)
    else:
        draw.polygon([(x,y-55),(x-60,y+50),(x+60,y+50)],fill=PINK)
        draw.line((x,y-18,x,y+20),fill="white",width=8)
        draw.ellipse((x-4,y+31,x+4,y+39),fill="white")
    d=8*math.sin(2*t)
    draw.ellipse((x+65+d,y-70,x+78+d,y-57),fill=PINK)

def background():
    im=Image.new("RGB",(W,H))
    d=ImageDraw.Draw(im)
    for y in range(H):
        d.line((0,y,W,y),fill=(12+int(y*6/H),10+int(y*3/H),29+int(y*19/H)))
    return im
BASE=background()
F_BIG=fnt(34,True)
F_CAP=fnt(20)
F_TAG=fnt(17,True)
F_SMALL=fnt(13,True)

def frame(t,chunks,bounds,duration):
    idx=min(len(chunks)-1,max(0,bisect.bisect_right(bounds,t)-1))
    seg=chunks[idx]
    img=BASE.copy()
    d=ImageDraw.Draw(img)
    for i in range(15):
        a=i*2.399+t*.17
        x=216+int(210*math.cos(a))
        y=420+int(270*math.sin(a+t*.05))
        d.ellipse((x-2,y-2,x+2,y+2),fill=(39,65,98))
    box(d,(19,31,W-19,75),14,(29,39,71),(52,77,110),2)
    d.text((35,43),"METON DIGITAL",font=F_TAG,fill="white")
    d.ellipse((W-58,42,W-38,62),fill=PINK)
    y=119
    for line in wrapped(d,seg["heading"].upper(),F_BIG,W-48)[:3]:
        d.text((24,y),line,font=F_BIG,fill="white")
        y+=44
    d.rectangle((24,y+7,24+int((W-48)*min(1,(t-bounds[idx])/max(.1,bounds[idx+1]-bounds[idx]))),y+12),fill=PINK)
    mascot(img,t)
    d=ImageDraw.Draw(img)
    scene_icon(d,seg,t)
    for i in range(2):
        a=5*i+4*t
        px=313+int(25*math.sin(a))
        py=489+73*i+int(9*math.cos(a))
        d.ellipse((px-15,py-15,px+15,py+15),fill=(45,60,106),outline=CYAN,width=2)
        d.line((px-7,py,px-1,py+7,px+9,py-9),fill="white",width=3)
    box(d,(18,619,W-18,716),19,(27,36,72),CYAN,2)
    subtitles=wrapped(d,seg["subtitle"],F_CAP,W-74)[:3]
    y=662-14*len(subtitles)
    for line in subtitles:
        d.text((36,y),line,font=F_CAP,fill=(251,252,255))
        y+=27
    d.text((21,735),"@metonalencar  •  APRENDA EM MOVIMENTO",font=F_SMALL,fill=(169,183,202))
    box(d,(20,756,W-20,760),2,(51,59,88))
    box(d,(20,756,20+int((W-40)*min(1,t/duration)),760),2,PINK)
    return img

def render_video(scenes,voice_file,target,duration,crf=27):
    chunks,bounds=segments(scenes,duration)
    total_frames=math.ceil((duration+.05)*FPS)
    target=Path(target)
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo",
         "-pixel_format","rgb24","-video_size",f"{W}x{H}",
         "-framerate",str(FPS),"-i","pipe:0",
         "-i",str(voice_file),"-t",f"{duration:.3f}",
         "-vf","fps=30,scale=720:1280:flags=lanczos,format=yuv420p",
         "-c:v","libx264","-preset","veryfast","-crf",str(crf),
         "-maxrate","1500k","-bufsize","3000k",
         "-c:a","aac","-b:a","96k","-movflags","+faststart",
         str(target)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(total_frames):
            process.stdin.write(frame(n/FPS,chunks,bounds,duration).tobytes())
    except BrokenPipeError as exc:
        raise RuntimeError("FFmpeg encerrou durante a renderização B+") from exc
    finally:
        if process.stdin:
            process.stdin.close()
    if process.wait()!=0 or not target.exists():
        raise RuntimeError("Falha ao gerar MP4 no estilo B+")
    return {"visual_format":"B+ NEXO","segments":len(chunks),"fps":30}
