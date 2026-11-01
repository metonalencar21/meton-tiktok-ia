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
    """Cortes curtos: cada tomada recebe uma frase enxuta, não um parágrafo."""
    chunks=[]
    for scene in scenes:
        sentences=[x.strip() for x in re.split(r"(?<=[.!?])\s+",scene["say"]) if x.strip()]
        for sentence in sentences:
            words=sentence.split()
            for i in range(0,len(words),8):
                phrase=" ".join(words[i:i+8])
                if phrase:
                    chunks.append({"heading":scene["heading"],"subtitle":phrase})
    weights=[max(3,len(c["subtitle"].split())) for c in chunks]
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

def story_kind(text):
    s=text.lower()
    if any(x in s for x in ("áudio","voz","ligação","clonad","familiar")): return "audio"
    if any(x in s for x in ("pix","pagamento","transferên","banco")): return "pix"
    if any(x in s for x in ("foto","imagem","galeria","câmera")): return "photo"
    if any(x in s for x in ("senha","código","seguran","proteção")): return "security"
    if any(x in s for x in ("wi-fi","rede pública","conexão")): return "wifi"
    if any(x in s for x in ("aplicativo","app","instal","permiss")): return "apps"
    if any(x in s for x in ("link","site","endereço","fraude")): return "link"
    if any(x in s for x in ("armazen","espaço","download","arquivo")): return "files"
    return "message"

def human_actor(d,x,y,t,stage):
    """Personagem humano estilizado, expressão e ação mudam conforme a cena."""
    hop=int(4*math.sin(t*3.1))
    y+=hop
    clothes=(60,126,179) if stage%3 else (224,98,132)
    # tronco / braços / mãos apontando para o telefone
    box(d,(x-66,y+49,x+67,y+183),30,clothes)
    d.line((x+38,y+85,x+72,y+113),fill=(232,169,131),width=18)
    d.ellipse((x+62,y+99,x+84,y+122),fill=(245,185,143))
    d.line((x-42,y+86,x-65,y+119),fill=(232,169,131),width=18)
    d.ellipse((x-78,y+110,x-55,y+133),fill=(245,185,143))
    # rosto e cabelo
    d.ellipse((x-48,y-52,x+48,y+66),fill=(242,187,147))
    d.pieslice((x-53,y-58,x+53,y+31),180,360,fill=(34,31,50))
    d.ellipse((x-42,y-18,x-33,y+1),fill=(247,201,159))
    d.ellipse((x+33,y-18,x+42,y+1),fill=(247,201,159))
    for dx in (-19,19):
        d.ellipse((x+dx-4,y-2,x+dx+4,y+7),fill=(31,38,58))
    if stage%3==0:
        d.ellipse((x-7,y+23,x+7,y+40),fill=(108,43,64))
    elif stage%3==1:
        d.arc((x-15,y+17,x+15,y+39),0,180,fill=(114,57,68),width=3)
    else:
        d.arc((x-15,y+16,x+15,y+39),180,355,fill=(114,57,68),width=3)

def phone_stage(d,x,y,t,kind,stage):
    """Telas encenadas com mudanças visuais: áudio, Pix, fotos, links, apps."""
    wave=math.sin(t*4)
    box(d,(x,y,x+166,y+302),23,(12,18,37),(178,207,232),4)
    box(d,(x+9,y+28,x+157,y+270),11,(236,244,251))
    box(d,(x+55,y+10,x+111,y+15),3,(112,141,173))
    d.text((x+19,y+40),"CELULAR",font=fnt(13,True),fill=(33,58,84))
    d.line((x+17,y+65,x+148,y+65),fill=(191,202,218),width=2)
    if kind=="audio":
        box(d,(x+17,y+88,x+145,y+155),12,(211,234,252))
        d.text((x+29,y+98),"AUDIO",font=fnt(16,True),fill=(42,67,112))
        d.polygon(((x+29,y+124),(x+29,y+145),(x+46,y+135)),fill=PINK)
        for i in range(10):
            h=7+int(11*abs(math.sin(t*3+i)))
            d.line((x+55+i*8,y+134-h,x+55+i*8,y+134+h),fill=(40,143,180),width=3)
        d.text((x+21,y+191),"CONFIRME",font=fnt(16,True),fill=(36,74,103))
    elif kind=="pix":
        d.text((x+31,y+86),"PIX",font=fnt(28,True),fill=(38,137,156))
        box(d,(x+20,y+134,x+146,y+183),9,(251,220,220))
        d.text((x+29,y+145),"VALOR?",font=fnt(18,True),fill=(143,49,64))
        d.text((x+24,y+204),"VERIFIQUE",font=fnt(14,True),fill=(34,81,107))
    elif kind=="photo":
        for i in range(4):
            xx=x+19+(i%2)*67
            yy=y+83+(i//2)*65
            box(d,(xx,yy,xx+60,yy+56),8,(116+20*i,177,207))
            d.ellipse((xx+12,yy+12,xx+28,yy+28),fill=(255,220,153))
            d.polygon(((xx+5,yy+50),(xx+27,yy+30),(xx+53,yy+50)),fill=(71,151,127))
        d.text((x+40,y+229),"FOTOS",font=fnt(14,True),fill=(48,75,97))
    elif kind=="security":
        d.text((x+35,y+83),"SENHA",font=fnt(17,True),fill=(42,67,103))
        box(d,(x+19,y+119,x+147,y+174),11,(211,231,248))
        for i in range(5):
            d.ellipse((x+30+i*22,y+140,x+40+i*22,y+150),fill=(46,72,111))
        d.text((x+27,y+210),"PROTEJA",font=fnt(15,True),fill=(33,111,109))
    elif kind=="wifi":
        for r in (48,35,22):
            d.arc((x+83-r,y+138-r//2,x+83+r,y+138+r),195,345,fill=(36,137,168),width=6)
        d.ellipse((x+78,y+171,x+88,y+181),fill=PINK)
        d.text((x+31,y+218),"REDE?",font=fnt(16,True),fill=(65,80,112))
    elif kind=="apps":
        for i in range(6):
            xx=x+19+(i%3)*46
            yy=y+88+(i//3)*56
            box(d,(xx,yy,xx+39,yy+39),9,((70+i*25)%190+40,120+i*12,182))
            d.ellipse((xx+12,yy+12,xx+27,yy+27),fill=(241,246,250))
        d.text((x+31,y+226),"REVISE",font=fnt(17,True),fill=(40,86,120))
    elif kind=="link":
        box(d,(x+15,y+98,x+151,y+145),8,(212,230,246))
        d.text((x+23,y+108),"SITE?",font=fnt(19,True),fill=(49,93,123))
        d.line((x+29,y+176,x+140,y+176),fill=PINK,width=5)
        d.text((x+29,y+196),"CHEQUE",font=fnt(15,True),fill=(38,104,120))
    elif kind=="files":
        for i in range(3):
            yy=y+88+i*47
            box(d,(x+20,yy,x+145,yy+33),7,(215,229,244))
            d.rectangle((x+29,yy+10,x+55,yy+23),fill=(49,153,165))
            d.line((x+67,yy+16,x+128,yy+16),fill=(106,130,162),width=4)
        d.text((x+29,y+238),"ORGANIZE",font=fnt(14,True),fill=(38,102,110))
    else:
        box(d,(x+20,y+90,x+146,y+163),10,(214,232,248))
        d.text((x+34,y+115),"NOVA",font=fnt(19,True),fill=(49,99,128))
        d.text((x+29,y+195),"MENSAGEM",font=fnt(13,True),fill=(59,91,122))
    # ação de toque/checagem no celular
    if stage%3==2:
        d.ellipse((x+129,y+205,x+146,y+222),fill=(47,166,129))
        d.line((x+131,y+212,x+136,y+217,x+143,y+207),fill="white",width=2)
    else:
        d.ellipse((x+126,y+203,x+145,y+223),fill=PINK)
        d.text((x+130,y+203),"!",font=fnt(15,True),fill="white")
    d.ellipse((x+78,y+282,x+88,y+292),fill=(125,147,174))
    # mão e indicador animado, simulando ação em vez de ícone estático
    ty=y+170+int(10*wave)
    d.line((x+181,ty+35,x+137,ty),fill=(241,185,143),width=11)
    d.ellipse((x+128,ty-8,x+145,ty+8),fill=(248,198,159))

def frame(t,chunks,bounds,duration):
    idx=min(len(chunks)-1,max(0,bisect.bisect_right(bounds,t)-1))
    seg=chunks[idx]
    stage=idx//3
    palette=[(10,20,45),(13,43,61),(38,20,51),(15,35,42),(36,27,58)]
    img=Image.new("RGB",(W,H),palette[stage%len(palette)])
    d=ImageDraw.Draw(img)
    # quadro muda entre tomadas, com movimento discreto de câmera e elementos
    pan=int(10*math.sin(t*.65))
    d.ellipse((-112+pan,200,248+pan,565),fill=(30,66,93))
    d.ellipse((255-pan,245,568-pan,610),fill=(43,45,92))
    for j in range(11):
        yy=80+j*59
        d.line((0,yy,W,yy+int(10*math.sin(t*.4+j))),fill=(35,54,81),width=1)
    box(d,(17,23,W-17,70),13,(21,40,65),(72,110,144),2)
    d.text((33,38),"METON DIGITAL",font=fnt(17,True),fill="white")
    d.text((W-105,42),"HISTORIA",font=fnt(11,True),fill=CYAN)
    d.text((23,88),f"CENA {idx+1:02d}/{len(chunks):02d}",font=fnt(14,True),fill=CYAN)
    yy=119
    heading=wrapped(d,seg["heading"].upper(),fnt(28,True),W-52)[:3]
    for line in heading:
        d.text((24,yy),line,font=fnt(28,True),fill=(246,249,255))
        yy+=38
    # alternância de plano e posição do personagem para dar progressão à história
    phone_right=stage%2==0
    px=240 if phone_right else 26
    hx=113 if phone_right else 315
    human_actor(d,hx,350,t,stage)
    kind=story_kind(seg["heading"]+" "+seg["subtitle"])
    phone_stage(d,px,279,t,kind,stage)
    # reação visual curta entre problema e solução
    status="ATENCAO" if stage%3==0 else ("VERIFIQUE" if stage%3==1 else "RESOLVIDO")
    accent=(251,125,129) if stage%3==0 else (CYAN if stage%3==2 else (255,209,122))
    box(d,(41,595,W-41,625),11,(19,31,54))
    d.text((58,601),status,font=fnt(15,True),fill=accent)
    box(d,(15,639,W-15,733),15,(14,26,47),(57,147,164),2)
    cap_font=fnt(21,True)
    cap=wrapped(d,seg["subtitle"],cap_font,W-62)[:3]
    cy=660+(3-len(cap))*10
    for line in cap:
        d.text((31,cy),line,font=cap_font,fill="white")
        cy+=27
    d.text((19,744),"@metonalencar",font=fnt(12,True),fill=(170,213,228))
    box(d,(134,748,W-18,753),2,(49,64,83))
    box(d,(134,748,134+int((W-152)*min(1,t/max(duration,.01))),753),2,PINK)
    # wipe rápido a cada mudança de plano
    dt=t-bounds[idx]
    if dt<.10:
        d.rectangle((0,0,int(W*(.10-dt)/.10),H),fill=(232,241,246))
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
         "-c:a","aac","-b:a","160k","-movflags","+faststart",
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
    return {"visual_format":"STORY 2D CENAS HUMANAS","segments":len(chunks),"fps":30}
