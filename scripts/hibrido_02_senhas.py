#!/usr/bin/env python3
"""Piloto HÍBRIDO 02: senhas diferentes por conta.
Personagem CGI 3D da identidade aprovada + demonstrações de celular
animadas em 2D. Imagens estáticas não são vídeo gerativo 3D; sem postagem.
"""
import json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/"public"/"assets"
OUT=ROOT/"public"/"pilotos"
OUT.mkdir(parents=True,exist_ok=True)
W,H,FPS=540,960,12
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
WHITE=(248,249,255)
PINK=(255,55,153)
CYAN=(62,232,237)
YELLOW=(255,221,93)
GREEN=(73,231,161)
RED=(255,80,110)
NAVY=(8,9,26)
STORY=[
 ("GANCHO","UMA SENHA SÓ?","Esse hábito pode abrir várias portas",
  "Você usa a mesma senha em vários aplicativos? Olha só o que pode acontecer se uma dessas contas sofrer um vazamento.","hook"),
 ("REUSO","MESMA SENHA EM TUDO","Uma falha afeta várias contas",
  "Imagine usar a mesma senha no e-mail, na loja online e nas redes sociais. Parece prático, mas é um risco.","accounts"),
 ("VAZAMENTO","UMA CONTA VAZOU","As outras podem estar expostas",
  "Se essa senha for descoberta em um serviço, alguém pode tentar usá-la nas suas outras contas também.","leak"),
 ("SOLUÇÃO","SENHAS DIFERENTES","Uma chave para cada conta",
  "A regra é simples: cada conta precisa de uma senha própria. Assim, um vazamento não entrega automaticamente as demais.","unique"),
 ("COMPRIMENTO","PREFIRA SENHAS LONGAS","Comprimento e exclusividade importam",
  "Uma senha longa e difícil de adivinhar costuma proteger mais. Evite nomes, datas de aniversário e sequências óbvias.","strength"),
 ("GERENCIADOR","NÃO PRECISA DECORAR","Use um gerenciador confiável",
  "Um gerenciador de senhas pode criar combinações exclusivas e guardar tudo de forma protegida, sem você precisar memorizar cada uma.","manager"),
 ("PROTEÇÃO EXTRA","ATIVE DUAS ETAPAS","Adicione uma segunda barreira",
  "E ative a verificação em duas etapas sempre que estiver disponível. Ela acrescenta uma proteção importante ao acesso.","mfa"),
 ("DEMONSTRAÇÃO","VEJA A DIFERENÇA","Um exemplo visual, não senha real",
  "Troque a senha repetida por combinações diferentes para cada aplicativo. Nunca compartilhe códigos de verificação recebidos por mensagem.","example"),
 ("LEMBRETE","TRÊS CUIDADOS","Diferente, longa e duas etapas",
  "Então lembra: senha diferente em cada conta, comprimento adequado e autenticação em duas etapas. São hábitos simples que ajudam muito.","recap"),
 ("ENCERRAMENTO","PROTEJA SUAS CONTAS","Salve e compartilhe esta dica",
  "Se essa dica foi útil, salva o vídeo e manda para alguém da família. Aqui tem mais segurança digital sem complicação.","cta")
]

def run(argv):
    return subprocess.run(argv,check=True,stdout=subprocess.DEVNULL)

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error",
             "-show_entries","format=duration:stream=codec_name,codec_type,width,height,r_frame_rate",
             "-of","json",str(path)]))

def textfont(px,bold=False):
    return ImageFont.truetype(BOLD if bold else FONT,px)
def rr(d,xy,r,fill,outline=None,w=1):
    d.rounded_rectangle(tuple(int(v) for v in xy),radius=r,fill=fill,outline=outline,width=w)
def txt(d,xy,word,size=22,color=WHITE,bold=True):
    d.text((int(xy[0]),int(xy[1])),word,font=textfont(size,bold),
           fill=color,stroke_width=1,stroke_fill=(5,7,18))
def fit(text):
    return [text[:28],text[28:]] if len(text)>28 else [text]

def img_source(path):
    im=Image.open(path).convert("RGB")
    scale=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    x=(im.width-W)//2;y=(im.height-H)//2
    return im.crop((x,y,x+W,y+H))

def background(t,hero,asset):
    if hero:
        im=asset.copy()
        dx=round(6*math.sin(t*.9));dy=round(5*math.cos(t*.65))
        return Image.new("RGB",(W,H),NAVY) if not im else im.transform((W,H),Image.Transform.AFFINE,
          (1,0,-dx,0,1,-dy),Image.Resampling.BICUBIC,fillcolor=NAVY)
    a=np.empty((H,W,3),dtype=np.uint8)
    top=np.array([11,8,32.])
    bottom=np.array([17,13,56.])
    yy=np.linspace(0,1,H)[:,None]
    a[:,:,:]=(top[None,None,:]*(1-yy[:,:,None])+bottom[None,None,:]*yy[:,:,None]).astype(np.uint8)
    return Image.fromarray(a,"RGB")

def phone(d,x=85,y=215,w=375,h=595):
    rr(d,(x-8,y-8,x+w+8,y+h+8),40,(25,28,54),PINK,4)
    rr(d,(x,y,x+w,y+h),33,(12,20,44),(64,228,240),3)
    rr(d,(x+w*.35,y+15,x+w*.65,y+31),10,(2,6,24))
    return x,y,w,h

def pill(d,xy,text,bg,fg=WHITE,size=19):
    x,y=xy
    tw=d.textbbox((0,0),text,font=textfont(size,True))[2]
    rr(d,(x,y,x+tw+28,y+38),14,bg)
    txt(d,(x+14,y+7),text,size,fg)

def short_caption(spoken,local,dt,max_words=7):
    """Seleciona uma legenda curta seguindo a narração, sem parágrafo fixo."""
    words=spoken.split()
    if not words:return ""
    chunks=[words[i:i+max_words] for i in range(0,len(words),max_words)]
    index=min(len(chunks)-1,int((local/max(.1,dt))*len(chunks)))
    return " ".join(chunks[index]).upper()

def action_pulse(d,x,y,t,color=CYAN):
    """Toque visível na interface: anel pulsante + ponto de contato."""
    phase=(t*2.2)%1
    radius=13+int(22*phase)
    alpha_color=tuple(int(c*(1-.45*phase)) for c in color)
    d.ellipse((x-radius,y-radius,x+radius,y+radius),outline=alpha_color,width=4)
    d.ellipse((x-7,y-7,x+7,y+7),fill=WHITE,outline=color,width=2)

def badge(d,x,y,word,amount,fill):
    rr(d,(x,y,x+amount,y+65),13,fill,(79,87,149),2)
    txt(d,(x+18,y+12),word,20)

def cell_demo(im,kind,local,dt,t):
    d=ImageDraw.Draw(im)
    phase=int((local/max(.1,dt))*4)
    progress=min(1.,local/1.1)
    if kind in ("accounts","unique","leak","example"):
        x,y,w,h=phone(d,70,210,400,575)
        apps=[("E-MAIL","MAIL"),("LOJA ONLINE","SHOP"),("REDE SOCIAL","SOCIAL")]
        for i,(title,alias) in enumerate(apps):
            yy=y+105+i*139
            rr(d,(x+24,yy,x+w-24,yy+114),17,(33,39,79),(79,92,146),2)
            rr(d,(x+39,yy+18,x+87,yy+68),13,
                 CYAN if i==0 else PINK if i==1 else (121,105,255))
            txt(d,(x+111,yy+12),title,17)
            label="••••••••" if kind in ("unique","example") else "SENHA 123"
            txt(d,(x+111,yy+55),label,23,YELLOW if kind in ("accounts","leak") else WHITE)
            if kind in ("unique","example"):
                visible=phase>=i
                rr(d,(x+w-81,yy+57,x+w-38,yy+96),12,GREEN if visible else (76,85,120))
                txt(d,(x+w-72,yy+63),"✓" if visible else "•",22,NAVY if visible else WHITE)
            elif kind=="leak":
                if phase>=i:
                    rr(d,(x+w-87,yy+55,x+w-39,yy+96),12,RED)
                    txt(d,(x+w-75,yy+61),"!",24)
        active=min(2,phase)
        action_pulse(d,x+w-59,y+105+active*139+76,t,RED if kind=="leak" else GREEN)
        txt(d,(x+43,y+48),"SUAS CONTAS",23)
        return
    if kind in ("manager","strength","mfa"):
        x,y,w,h=phone(d,70,202,400,586)
        title={"manager":"COFRE DE SENHAS","strength":"CRIAR SENHA","mfa":"VERIFICAÇÃO EXTRA"}[kind]
        txt(d,(x+35,y+70),title,21)
        if kind=="strength":
            rr(d,(x+29,y+165,x+w-29,y+246),16,(37,43,83),(98,115,161),2)
            passwd="••••••••••••••••••"[:int(6+13*progress)]
            txt(d,(x+54,y+183),passwd,27)
            rr(d,(x+30,y+291,x+w-30,y+315),12,(60,69,109))
            rr(d,(x+30,y+291,x+30+int((w-60)*max(.2,local/dt)),y+315),12,GREEN)
            txt(d,(x+36,y+355),"LONGA + EXCLUSIVA",20,CYAN)
            pill(d,(x+42,y+446),"EVITE DADOS PESSOAIS",(26,100,113),WHITE,16)
            action_pulse(d,x+w-70,y+302,t,GREEN)
        elif kind=="manager":
            rr(d,(x+111,y+158,x+266,y+318),28,(49,56,105),CYAN,4)
            d.arc((x+148,y+130,x+231,y+238),175,365,fill=CYAN,width=12)
            d.ellipse((x+174,y+227,x+202,y+255),fill=YELLOW)
            for k,word in enumerate(("E-mail","Loja","Rede social")):
                rr(d,(x+45,y+365+k*59,x+w-45,y+410+k*59),12,(33,45,82),(74,109,156))
                txt(d,(x+59,y+373+k*59),word,18)
                txt(d,(x+w-75,y+375+k*59),"✓",22,GREEN)
            action_pulse(d,x+w-62,y+389+min(2,phase)*59,t,GREEN)
        else:
            txt(d,(x+54,y+163),"Seu código de acesso",20)
            for i in range(6):
                sx=x+45+i*51
                rr(d,(sx,y+225,sx+43,y+286),11,(37,47,84),(79,107,151),2)
                if phase>=i//2: txt(d,(sx+12,y+239),"•",26,CYAN)
            rr(d,(x+49,y+354,x+w-49,y+417),15,GREEN)
            txt(d,(x+103,y+373),"CONFIRMAR",20,NAVY)
            pill(d,(x+35,y+466),"NÃO ENVIE O CÓDIGO", (106,39,70),WHITE,17)
            action_pulse(d,x+66+min(5,phase+1)*51,y+255,t,CYAN)
        return
    if kind in ("recap","cta"):
        for i,(icon,word) in enumerate([("1","SENHAS DIFERENTES"),("2","SENHAS LONGAS"),("3","DUAS ETAPAS")]):
            w=440
            yy=258+i*141
            rr(d,(50,yy,490,yy+98),18,(29,33,75),CYAN if phase>=i else (99,83,144),3)
            rr(d,(73,yy+18,126,yy+74),15,PINK)
            txt(d,(90,yy+31),icon,23)
            txt(d,(151,yy+34),word,18)
        return
    # Intro hero: notification appearing over the CGI presenter.
    rr(d,(32,577,508,707),20,(19,24,54),(254,80,153),3)
    txt(d,(61,600),"MESMA SENHA EM TUDO?",24,YELLOW)
    if phase>=1:txt(d,(65,658),"NÃO É UMA BOA IDEIA!",21,CYAN)

def show_frame(global_t,part_durations,cutoffs,master,senha):
    idx=next((k for k in range(len(part_durations)) if cutoffs[k]<=global_t<cutoffs[k+1]),len(part_durations)-1)
    headline,tag,detail,spoken,kind=STORY[idx]
    local=global_t-cutoffs[idx];dt=part_durations[idx]
    hero=kind in ("hook","cta")
    src=master if hero else senha
    im=background(global_t,hero,src)
    if not hero:
       # Soft neon particles moving across a genuine CGI scene for hybrid aesthetics.
       im=Image.blend(im,Image.new("RGB",(W,H),NAVY),.68)
    d=ImageDraw.Draw(im)
    for j in range(12):
       px=(j*61+int(global_t*5))%W
       py=(j*151+int(global_t*14))%H
       d.ellipse((px-2,py-2,px+2,py+2),fill=CYAN if j%2 else PINK)
    rr(d,(18,21,522,78),15,(12,16,37),PINK,2)
    txt(d,(36,34),"METON DIGITAL",23)
    txt(d,(410,42),"100% IA",14,PINK)
    if idx>0:
        rr(d,(18,90,522,173),17,(16,16,45),(88,93,143),2)
        txt(d,(36,99),tag,26,YELLOW if kind=="leak" else CYAN)
        txt(d,(37,139),detail,14,WHITE)
    cell_demo(im,kind,local,dt,global_t)
    d=ImageDraw.Draw(im)
    caption=short_caption(spoken,local,dt)
    rr(d,(22,778,518,837),15,(6,10,29),(255,55,153),2)
    txt(d,(36,793),caption[:43],16,WHITE)
    rr(d,(22,851,518,909),15,(10,13,33),(57,221,226),2)
    phrase="SENHA ÚNICA = MAIS SEGURANÇA" if idx<8 else "SALVE  •  COMPARTILHE  •  SIGA"
    txt(d,(34,867),phrase,17,WHITE)
    rr(d,(24,927,516,936),4,(59,65,108))
    rr(d,(24,927,24+int(492*min(1,global_t/cutoffs[-1])),936),4,PINK)
    return im

def main():
    master=img_source(ASSET/"personagem-mestre.jpg")
    senha=img_source(ASSET/"personagem-senhas.jpg")
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        parts=[]
        lens=[]
        for i,(_,_,_,speech,_) in enumerate(STORY):
            path=tmp/f"narracao_{i:02d}.mp3"
            run(["edge-tts","--voice","pt-BR-FranciscaNeural","--rate=-10%",
                 "--text",speech,"--write-media",str(path)])
            duration=float(probe(path)["format"]["duration"])
            if duration<3: raise RuntimeError(f"Narração curta ou ausente no trecho {i+1}")
            parts.append(path);lens.append(duration)
        playlist=tmp/"playlist.ffconcat"
        playlist.write_text("ffconcat version 1.0\n"+"\n".join("file '"+str(p)+"'" for p in parts)+"\n",encoding="utf-8")
        audio=tmp/"voz.mp3"
        run(["ffmpeg","-y","-loglevel","error","-safe","0","-f","concat","-i",
             str(playlist),"-c:a","libmp3lame","-b:a","128k",str(audio)])
        cutoffs=[0.]
        for x in lens:cutoffs.append(cutoffs[-1]+x)
        full=float(probe(audio)["format"]["duration"])
        if full<55: raise RuntimeError(f"Roteiro ficou curto: {full}s")
        target=OUT/"hibrido_02_senhas_diferentes.mp4"
        command=["ffmpeg","-y","-loglevel","error","-f","rawvideo",
                 "-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0",
                 "-i",str(audio),"-t",f"{full:.3f}","-vf","fps=30,scale=720:1280:flags=lanczos,format=yuv420p",
                 "-c:v","libx264","-preset","veryfast","-crf","25",
                 "-c:a","aac","-b:a","128k","-movflags","+faststart",str(target)]
        process=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for i in range(math.ceil(full*FPS)):
                frame=show_frame(i/FPS,lens,cutoffs,master,senha)
                process.stdin.write(frame.tobytes())
        except BrokenPipeError as exc:
            raise RuntimeError("Falha no FFmpeg ao criar animação") from exc
        finally:
            process.stdin.close()
        if process.wait()!=0 or not target.exists():raise RuntimeError("MP4 não foi produzido")
        stats=probe(target)
        streams=stats["streams"]
        vid=next(s for s in streams if s.get("codec_type")=="video")
        aud=next(s for s in streams if s.get("codec_type")=="audio")
        assert vid["width"]==720 and vid["height"]==1280 and vid["codec_name"]=="h264" and aud["codec_name"]=="aac"
        meta={"title":"Uma senha diferente por conta",
              "profile":"@metonalencar","visual_style":"HÍBRIDO CGI + CELULAR ANIMADO",
              "narration":"pt-BR-FranciscaNeural",
              "duration_s":round(float(stats["format"]["duration"]),1),
              "scene_count":len(STORY),"format":"720x1280 H264 AAC 30fps",
              "source_assets":["public/assets/personagem-mestre.jpg","public/assets/personagem-senhas.jpg"],
              "approved":False,"published":False,"scheduled":False,
              "status":"review_only",
              "note":"Personagem usa imagem CGI animada em 2.5D. Não há atuação 3D com sincronização labial."}
        (OUT/"hibrido_02_senhas_diferentes.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
        print("HIBRIDO_SENHAS_OK",meta,"bytes",target.stat().st_size,flush=True)
if __name__=="__main__":main()

# Render revision 2026-11-23: ações e legendas dinâmicas.
