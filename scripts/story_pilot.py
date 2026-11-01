#!/usr/bin/env python3
"""Piloto editorial 2: história visual de golpe com voz clonada.

O vídeo encena uma conversa FICTÍCIA, sem logos, capturas de apps reais,
fotografias de terceiros ou material protegido. Nunca publica nem agenda.
"""
import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from produce import make_voice, probe, seconds

W, H, FPS = 432, 768, 12
ROOT = Path(__file__).resolve().parents[1]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BG = (7, 13, 29)
WHITE = (243, 248, 255)
MUTED = (167, 190, 213)
CYAN = (69, 231, 215)
PINK = (255, 77, 146)
AMBER = (255, 196, 98)
RED = (255, 97, 109)

STORY = [
    {
        "slug": "audio", "tag": "01 · A MENSAGEM", "title": "UMA VOZ CONHECIDA",
        "narration": "Imagina receber um áudio com a voz de alguém da sua família. Parece a voz certa, com o jeito de falar que você conhece.",
        "callout": "ÁUDIO RECEBIDO"
    },
    {
        "slug": "request", "tag": "02 · A PRESSÃO", "title": "PEDIDO URGENTE",
        "narration": "A pessoa diz que teve uma emergência e precisa de um Pix agora. Ela pede que você não ligue, porque está sem tempo.",
        "callout": "FAZ UM PIX AGORA?"
    },
    {
        "slug": "clone", "tag": "03 · O RISCO", "title": "PODE SER UMA IMITAÇÃO",
        "narration": "Só que existe um problema: ferramentas de inteligência artificial conseguem imitar características de uma voz. Ouvir alguém conhecido não é prova de identidade.",
        "callout": "VOZ REAL OU CLONADA?"
    },
    {
        "slug": "stop", "tag": "04 · PRIMEIRA AÇÃO", "title": "NÃO TRANSFIRA",
        "narration": "Por isso, se receber um pedido inesperado de dinheiro, não faça a transferência durante a conversa. Pare, mesmo que o áudio pareça convincente.",
        "callout": "PARE ANTES DO PIX"
    },
    {
        "slug": "call", "tag": "05 · CONFIRME", "title": "LIGUE PARA O CONTATO",
        "narration": "Abra seus contatos e ligue para o número que você já tinha salvo. Não use um telefone novo enviado junto com a mensagem suspeita.",
        "callout": "USE O NÚMERO SALVO"
    },
    {
        "slug": "answer", "tag": "06 · A DESCOBERTA", "title": "ERA UMA TENTATIVA",
        "narration": "Se o familiar disser que não pediu dinheiro, você identificou um possível golpe. Avise a pessoa e não responda mais à mensagem suspeita.",
        "callout": "A PESSOA NÃO PEDIU PIX"
    },
    {
        "slug": "steps", "tag": "07 · NA PRÁTICA", "title": "TRÊS REGRAS SIMPLES",
        "narration": "Guarde três regras: desconfie da urgência, confirme por outro canal e nunca compartilhe códigos de segurança. Converse com sua família sobre esse tipo de golpe.",
        "callout": "PARE · LIGUE · CONFIRME"
    },
    {
        "slug": "end", "tag": "08 · RESUMO", "title": "ANTES DE PAGAR...",
        "narration": "Lembre: uma voz conhecida não garante que seja a pessoa verdadeira. Salve este vídeo e compartilhe com quem precisa se proteger.",
        "callout": "CONFIRME PRIMEIRO"
    },
]


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


F_TITLE = font(31, True)
F_TAG = font(14, True)
F_BODY = font(19)
F_CAP = font(21, True)
F_SMALL = font(13, True)
F_MID = font(17, True)
F_BIG = font(38, True)


def rect(d, bbox, r=12, fill=(20, 35, 59), outline=None, width=1):
    d.rounded_rectangle(tuple(int(a) for a in bbox), radius=r, fill=fill, outline=outline, width=width)


def center(d, xy, message, f, color=WHITE):
    bbox = d.textbbox((0, 0), message, font=f)
    d.text((int(xy[0] - (bbox[2] - bbox[0])/2), int(xy[1] - (bbox[3] - bbox[1])/2)), message, font=f, fill=color)


def wrap(d, words, f, width):
    result = []
    line = ""
    for word in words.split():
        test = (line + " " + word).strip()
        if line and d.textbbox((0, 0), test, font=f)[2] > width:
            result.append(line)
            line = word
        else:
            line = test
    if line:
        result.append(line)
    return result


def ease(x):
    x = min(1., max(0., x))
    return 1 - (1-x)**3


def alpha_in(local):
    return ease(local / .42)


def bubble(d, x, y, w, h, color, text, delay=0., local=0., dark=False):
    move = int(36 * (1-ease((local-delay)/.48)))
    rect(d, (x, y+move, x+w, y+h+move), 17, color)
    lines = wrap(d, text, F_MID, w-24)
    for i, line in enumerate(lines[:3]):
        d.text((x+12,y+move+12+i*25),line,font=F_MID,fill=BG if dark else WHITE)


def audio_wave(d, x, y, n, t, color=CYAN, step=10, height=35):
    for i in range(n):
        h = 6 + int(height * (.22 + .78 * abs(math.sin(i*1.6+t*4.2)*math.sin(i*.36+t*.86))))
        d.line((x+i*step,y-h/2,x+i*step,y+h/2),fill=color,width=4)


def phone(d, x, y, w=306, h=438, title="CONVERSA", t=0.):
    rect(d,(x+5,y+12,x+w+5,y+h+12),33,(2,5,15))
    rect(d,(x,y,x+w,y+h),32,(21,31,51),outline=(121,159,191),width=3)
    rect(d,(x+10,y+16,x+w-10,y+h-14),23,(232,241,247))
    rect(d,(x+10,y+16,x+w-10,y+83),22,(30,58,75))
    d.ellipse((x+24,y+34,x+65,y+75),fill=(112,186,199))
    center(d,(x+44,y+53),"M",F_MID,BG)
    d.text((x+78,y+35),title,font=F_MID,fill=WHITE)
    d.text((x+79,y+60),"mensagem privada",font=F_SMALL,fill=(179,217,229))
    d.line((x+70,y+h-36,x+w-70,y+h-36),fill=(92,113,135),width=4)
    return x+12,y+88,w-24,h-112


def warning(d, x, y, size=52, t=0.):
    glow = int(3*math.sin(t*5))
    d.ellipse((x-size//2-glow,y-size//2-glow,x+size//2+glow,y+size//2+glow),fill=(112,39,55))
    d.polygon([(x,y-size*.32),(x-size*.32,y+size*.28),(x+size*.32,y+size*.28)],fill=RED)
    center(d,(x,y+4),"!",F_MID,WHITE)


def check(d,x,y,size=54):
    d.ellipse((x-size/2,y-size/2,x+size/2,y+size/2),fill=(20,118,107))
    d.line((x-size*.24,y,x-size*.04,y+size*.20,x+size*.25,y-size*.20),fill=WHITE,width=7)


def circle_avatar(d, x, y, r, shade=(87,150,189)):
    d.ellipse((x-r,y-r,x+r,y+r),fill=shade)
    d.ellipse((x-r*.35,y-r*.60,x+r*.35,y+r*.08),fill=(248,199,154))
    d.pieslice((x-r*.38,y-r*.62,x+r*.38,y-r*.10),180,360,fill=(43,46,62))
    d.pieslice((x-r*.69,y-r*.02,x+r*.69,y+r*.96),185,355,fill=(35,68,105))


def draw_beat(d, slug, local, duration, i, t):
    appear = alpha_in(local)
    bob = int(5*math.sin(t*2.1))
    if slug == "audio":
        x,y,w,h = phone(d,57,175+bob,title="PESSOA CONHECIDA",t=t)
        bubble(d,x+12,y+34,w-24,120,(201,223,236),"Recebi um áudio de família.",local=local,dark=True)
        rect(d,(x+17,y+177,x+w-17,y+285),18,(210,230,242))
        d.ellipse((x+29,y+205,x+81,y+257),fill=(15,151,145))
        d.polygon([(x+51,y+217),(x+51,y+244),(x+70,y+230)],fill=WHITE)
        audio_wave(d,x+100,y+230,13,t,(26,139,157),9,30)
        d.text((x+112,y+265),"0:13",font=F_SMALL,fill=(51,87,108))
        rect(d,(32,110,400,157),15,(26,59,76),outline=(54,153,176),width=2)
        center(d,(216,132),"PARECE TÃO REAL...",F_MID,CYAN)
    elif slug == "request":
        x,y,w,h=phone(d,57,168+bob,title="PESSOA CONHECIDA")
        bubble(d,x+14,y+35,w-26,83,(218,231,241),"Preciso de ajuda!",local=local,dark=True)
        bubble(d,x+14,y+142,w-26,98,(225,89,105),"Faz um Pix de R$ 680 AGORA?",delay=.35,local=local)
        warning(d,338,557,61,t)
        rect(d,(58,110,373,153),14,(89,34,48))
        center(d,(215,131),"URGÊNCIA É SINAL DE ALERTA",F_TAG,WHITE)
    elif slug == "clone":
        rect(d,(24,190,408,527),25,(21,37,64),outline=(57,94,122),width=2)
        rect(d,(40,208,392,336),15,(24,75,91))
        rect(d,(40,363,392,505),15,(96,36,64))
        d.text((55,222),"VOZ QUE VOCÊ CONHECE",font=F_TAG,fill=WHITE)
        d.text((55,376),"VOZ QUE PODE SER IMITADA",font=F_TAG,fill=WHITE)
        audio_wave(d,65,292,31,t,CYAN,10,34)
        audio_wave(d,65,448,31,t+.15,PINK,10,34)
        rect(d,(82,535,352,594),16,(90,38,60))
        center(d,(216,566),"SÓ A VOZ NÃO BASTA",F_MID,WHITE)
    elif slug == "stop":
        rect(d,(36,204,396,514),32,(43,29,50),outline=(165,64,84),width=3)
        center(d,(216,290),"PIX",F_BIG,(231,230,241))
        center(d,(216,344),"R$ 680,00",F_BIG,WHITE)
        rect(d,(87,400,345,467),17,(114,48,63))
        center(d,(216,433),"TRANSFERIR",F_CAP,(246,195,201))
        d.line((69,400+int(7*math.sin(t*2)),360,464),fill=RED,width=11)
        warning(d,216,198,93,t)
        center(d,(216,557),"NÃO FAÇA NA PRESSA",F_CAP,RED)
    elif slug == "call":
        rect(d,(39,161,393,582),29,(25,48,72),outline=(77,122,158),width=3)
        circle_avatar(d,216,246,72)
        center(d,(216,353),"CONTATO JÁ SALVO",F_CAP,WHITE)
        center(d,(216,387),"Ligação normal",F_BODY,MUTED)
        for j in range(3):
            rr=35+j*17+(t*17)%15
            d.arc((216-rr,433-rr,216+rr,433+rr),195,345,fill=(44+8*j,157,151),width=3)
        d.ellipse((167,467,265,564),fill=(23,167,123))
        # handset icon
        d.arc((184,482,248,546),0,180,fill=WHITE,width=12)
        d.ellipse((180,505,200,528),fill=WHITE)
        d.ellipse((231,505,251,528),fill=WHITE)
        center(d,(216,609),"OUTRO CANAL = CONFIRMAÇÃO",F_TAG,CYAN)
    elif slug == "answer":
        x,y,w,h=phone(d,57,173+bob,title="CONTATO SALVO")
        bubble(d,x+15,y+62,w-30,86,(27,140,133),"Você pediu um Pix?",local=local)
        bubble(d,x+15,y+182,w-30,102,(208,228,238),"Não! Não pedi dinheiro.",delay=.35,local=local,dark=True)
        check(d,218,566,76)
        center(d,(216,619),"GOLPE IDENTIFICADO",F_TAG,CYAN)
    elif slug == "steps":
        items=[
            ("01","PARE","Não pague na pressão",RED),
            ("02","LIGUE","Use o contato salvo",AMBER),
            ("03","CONFIRME","Confira por outro canal",CYAN),
        ]
        for k,(number,title,detail,color) in enumerate(items):
            shift=int(46*(1-ease((local-k*.28)/.45)))
            yy=192+k*137+shift
            active=(int(local*1.1)%3)==k
            rect(d,(28,yy,404,yy+112),18,(23,42,64),outline=color if active else (46,75,96),width=3 if active else 1)
            d.ellipse((44,yy+22,106,yy+84),fill=color)
            center(d,(75,yy+52),number,F_MID,BG)
            d.text((126,yy+19),title,font=F_CAP,fill=WHITE)
            d.text((127,yy+55),detail,font=F_SMALL,fill=MUTED)
        center(d,(216,633),"TRÊS PASSOS QUE PROTEGEM",F_TAG,CYAN)
    else:
        rect(d,(28,185,404,576),30,(18,55,65),outline=(51,145,155),width=3)
        check(d,216,279,112)
        center(d,(216,395),"VOZ NÃO É PROVA",F_BIG,WHITE)
        center(d,(216,444),"CONFIRME ANTES",F_CAP,CYAN)
        center(d,(216,479),"DE TRANSFERIR",F_CAP,CYAN)
        rect(d,(71,528,361,570),15,(35,100,102))
        center(d,(216,548),"SALVE E COMPARTILHE",F_TAG,WHITE)


def caption_for(scene, local, duration):
    words=scene["narration"].split()
    if not words:
        return ""
    # Pequena janela de palavras para a legenda não reproduzir parágrafos inteiros.
    window=8
    step=max(1, math.ceil(len(words)/window))
    slot=min(step-1,int(local/max(duration,.01)*step))
    return " ".join(words[slot*window:(slot+1)*window])


def make_background():
    im=Image.new("RGB",(W,H))
    p=im.load()
    for y in range(H):
        for x in range(W):
            beam=max(0.,1-(((x-330)/320)**2+((y-145)/550)**2))
            p[x,y]=(int(8+12*beam),int(14+28*beam),int(30+44*beam))
    return im


BASE=make_background()


def frame(t, starts, duration):
    import bisect
    idx=max(0,min(len(STORY)-1,bisect.bisect_right(starts,t)-1))
    local=t-starts[idx]
    segduration=max(.01,starts[idx+1]-starts[idx])
    scene=STORY[idx]
    im=BASE.copy()
    d=ImageDraw.Draw(im)
    for k in range(11):
        sy=80+k*65+int(7*math.sin(t*.55+k))
        d.line((0,sy,W,sy),fill=(21,37,58),width=1)
    for k in range(10):
        x=(k*73+int(7*t))%W
        y=(k*119+int(4*t))%H
        d.ellipse((x-2,y-2,x+2,y+2),fill=(41,83,104))
    # Código visual: título objetivo, cena central, legendas curtas.
    rect(d,(18,20,414,66),14,(15,32,50),outline=(47,100,123),width=2)
    d.text((33,35),"METON DIGITAL",font=F_TAG,fill=WHITE)
    d.text((337,35),"HISTÓRIA",font=F_SMALL,fill=CYAN)
    d.text((25,90),scene["tag"],font=F_TAG,fill=CYAN)
    lines=wrap(d,scene["title"],F_TITLE,382)[:2]
    for n,line in enumerate(lines):
        d.text((24,118+n*38),line,font=F_TITLE,fill=WHITE)
    draw_beat(d,scene["slug"],local,segduration,idx,t)
    # Subtítulos se atualizam várias vezes, no máximo duas linhas.
    rect(d,(15,654,417,738),17,(6,13,30),outline=(72,149,165),width=2)
    caption=caption_for(scene,local,segduration)
    words=wrap(d,caption,F_BODY,363)[:2]
    for n,line in enumerate(words):
        center(d,(216,686+n*26),line,F_BODY,WHITE)
    d.text((19,745),"@metonalencar",font=F_SMALL,fill=MUTED)
    rect(d,(154,749,411,754),3,(35,50,68))
    rect(d,(154,749,154+max(1,int(257*min(1,t/max(.01,duration)))),754),3,PINK)
    # wipe rápido apenas na troca de cena
    if local<.11 and idx:
        opacity=(.11-local)/.11
        d.rectangle((0,0,int(W*opacity),H),fill=(33,68,81))
    return im


def render_story(audio, starts, target, duration):
    target=Path(target)
    target.parent.mkdir(parents=True,exist_ok=True)
    nframes=math.ceil(duration*FPS)
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pixel_format","rgb24",
         "-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","pipe:0",
         "-i",str(audio),"-t",f"{duration:.3f}",
         "-vf","fps=30,scale=720:1280:flags=lanczos,format=yuv420p",
         "-c:v","libx264","-preset","veryfast","-crf","24",
         "-c:a","aac","-b:a","160k","-movflags","+faststart",str(target)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(nframes):
            process.stdin.write(frame(n/FPS,starts,duration).tobytes())
    except BrokenPipeError as e:
        raise RuntimeError("FFmpeg interrompeu o render do piloto") from e
    finally:
        if process.stdin:
            process.stdin.close()
    if process.wait()!=0 or not target.is_file():
        raise RuntimeError("Falha ao renderizar filme")
    return target


def build(target):
    target=Path(target).resolve()
    with tempfile.TemporaryDirectory(prefix="meton_story_") as temp:
        tmp=Path(temp)
        # make_voice gera WAV por CENA: sincronização medida em vez de estimativa por palavras.
        joined="\n\n".join(s["narration"] for s in STORY)
        voice=tmp/"voice.mp3"
        engine=make_voice(joined,voice,"edge")
        if engine!="edge-tts":
            raise RuntimeError("A voz neural é obrigatória")
        duration=seconds(voice)
        starts=[0.]
        for i in range(len(STORY)):
            wav=tmp/f"speech_{i:02d}.wav"
            if not wav.exists():
                raise RuntimeError(f"Faltou trecho de áudio {i}")
            starts.append(starts[-1]+seconds(wav))
        # Compensar diferenças mínimas de codificação MP3.
        starts=[x*duration/starts[-1] for x in starts]
        if duration<70 or duration>120:
            raise RuntimeError(f"Duração editorial inesperada: {duration:.1f}s")
        render_story(voice,starts,target,duration)
    check=probe(target)
    aud=[x for x in check["streams"] if x["codec_type"]=="audio"]
    vid=[x for x in check["streams"] if x["codec_type"]=="video"]
    from fractions import Fraction
    assert len(aud)==len(vid)==1
    assert vid[0]["codec_name"]=="h264"
    assert vid[0]["width"]==720 and vid[0]["height"]==1280
    assert Fraction(vid[0]["avg_frame_rate"])==30
    assert seconds(target)>=70
    result={"title":"Cuidado com a voz clonada — história visual v2",
            "duration_s":round(seconds(target),1),
            "voice_engine":engine,
            "visual_format":"STORY V2 - ENCENAÇÃO DE MENSAGEM E VERIFICAÇÃO",
            "scenes":len(STORY),
            "animated":True,
            "quality_review_required":True,
            "approved":False,
            "published":False,
            "source":"story_pilot.py",
            "review_instructions":"Avaliar áudio e clareza de cada cena. Não usar somente teste de codec."}
    metadata=target.with_suffix(".json")
    metadata.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default=str(ROOT/"public/pilotos/historia-voz-clonada-v2.mp4"))
    options=parser.parse_args()
    build(options.output)


if __name__=="__main__":
    main()
