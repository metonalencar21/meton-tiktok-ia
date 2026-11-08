#!/usr/bin/env python3
"""Piloto de linguagem visual com imagens CGI consistentes e cenas dinâmicas.
NÃO é animação 3D de malha; usa duas imagens 3D renderizadas + movimento 2.5D,
UI animada, gestos visuais, boca aproximada e narração neural pt-BR.
NUNCA publica; exige aprovação humana. Sem API paga.
"""
import json, math, os, subprocess, tempfile
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"public"/"assets"
OUTPUT=ROOT/"public"/"pilotos"
OUTPUT.mkdir(parents=True,exist_ok=True)
A=ASSETS/"personagem-mestre.jpg"
B=ASSETS/"personagem-pix-alerta.jpg"
W,H,RENDER_FPS=540,960,12
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
COLOR={"white":(252,252,255),"pink":(251,47,139),"yellow":(255,218,50),
       "cyan":(64,231,241),"red":(255,76,94),"green":(57,230,167)}

def run(command, **kwargs):return subprocess.run(command,check=True,**kwargs)
def f(size,bold=True):return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)
def rect(d,bb,rad,fill,outline=None,width=1):
    d.rounded_rectangle(tuple(int(v) for v in bb),radius=rad,fill=fill,outline=outline,width=width)
def ease(x): x=max(0,min(1,x));return 1-(1-x)**3
def write(d,xy,message,size,color):
    d.text(xy,message,font=f(size),fill=color,stroke_fill=(9,4,21),stroke_width=1)
def read_image(path):
    if not path.exists() or path.stat().st_size<12000:raise RuntimeError("Falta imagem-mestre: "+str(path))
    im=Image.open(path).convert("RGB")
    ratio=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
    x=(im.width-W)//2;y=(im.height-H)//2
    return np.asarray(im.crop((x,y,x+W,y+H))).copy()

def info(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
    "format=duration:stream=codec_name,codec_type,width,height,avg_frame_rate",
    "-of","json",str(path)],text=True))
def speech(path):
    txt=("Recebeu um pedido de Pix urgente? Para agora. "
         "Foto conhecida não é prova de identidade. "
         "Antes de transferir dinheiro, ligue para o contato que você já tinha salvo. "
         "Confirme com a pessoa por outro caminho. "
         "Salva esta dica e compartilha com a família.")
    run(["edge-tts","--voice","pt-BR-FranciscaNeural","--rate=-5%",
         "--text",txt,"--write-media",str(path)],timeout=120)
    return txt

def mouth_motion(base,t,amount=1):
    # Microdeformação local dos lábios, sem substituir/distorcer o rosto.
    rh,rw=75,128;cx,cy=287,307
    x0,y0=cx-rw//2,cy-rh//2
    x1,y1=x0+rw,y0+rh
    patch=base[y0:y1,x0:x1].copy()
    if patch.shape[:2]!=(rh,rw):return base
    yy,xx=np.indices((rh,rw),dtype=np.float32)
    mask=np.exp(-(((xx-rw/2)/(rw*.32))**2 + ((yy-rh/2)/(rh*.38))**2)*1.8)
    strength=amount*(.3+.7*abs(math.sin(2*math.pi*3.6*t)))
    mx=xx.copy();my=yy-3.2*strength*mask*np.sign(yy-rh/2)
    warped=cv2.remap(patch,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    base[y0:y1,x0:x1]=np.clip(patch*(1-.6*mask[...,None])+warped*.6*mask[...,None],0,255).astype(np.uint8)
    return base

def phone(t,sec):
    im=Image.new("RGBA",(308,494),(0,0,0,0))
    d=ImageDraw.Draw(im)
    rect(d,(18,12,291,485),35,(6,9,26,251),(72,227,246,255),4)
    rect(d,(29,28,280,470),27,(25,29,57,251),(238,60,151,255),2)
    rect(d,(109,39,193,56),7,(0,0,0,255))
    write(d,(52,85),"MENSAGEM",24,COLOR["white"])
    rect(d,(46,154,270,273),14,(94,27,67,251),(255,90,132,255),3)
    write(d,(61,171),"OI, ME AJUDA?",17,COLOR["white"])
    write(d,(61,211),"PIX URGENTE!",22,COLOR["yellow"])
    rect(d,(42,328,278,391),12,(36,48,80,250),(120,138,182,255),2)
    write(d,(58,343),"CONFIRME ANTES",17,COLOR["cyan"])
    rect(d,(66,413,247,459),10,(47,188,126,255))
    write(d,(107,421),"LIGAR",19,COLOR["white"])
    im=im.rotate(-4+2*math.sin(t*1.2),Image.Resampling.BICUBIC,expand=True)
    return im

def draw_scene(t,total,master,alert):
    segment=min(3,int(4*t/total))
    progress=(4*t/total)-segment
    source=alert if segment in (1,2) else master
    # Continuous movement of the scene, separate from cinematic image quality.
    mat=cv2.getRotationMatrix2D((W*.5,H*.40),.7*math.sin(t*1.0),1.02+.006*math.sin(t*.7))
    mat[0,2]+=5*math.sin(1.2*t);mat[1,2]+=3*math.cos(.9*t)
    base=cv2.warpAffine(source,mat,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    if segment in (0,3):base=mouth_motion(base,t)
    overlay=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(overlay)
    # Header fixed inside safe TikTok area; short captions, no paragraph slides.
    rect(d,(18,22,522,71),14,(8,10,32,236),(251,47,139,255),2)
    write(d,(35,36),"@METONALENCAR  •  DICAS DIGITAIS",18,COLOR["white"])
    captions=[
      ("PEDIDO DE PIX?","NÃO TRANSFIRA NA PRESSA!",COLOR["yellow"]),
      ("GOLPE POR MENSAGEM","FOTO E NOME NÃO COMPROVAM!",COLOR["red"]),
      ("CONFIRME POR LIGAÇÃO","USE O CONTATO QUE JÁ ESTÁ SALVO",COLOR["cyan"]),
      ("ANTES DE PAGAR...","PARE, LIGUE E CONFIRME.",COLOR["green"])
    ]
    title,subtitle,highlight=captions[segment]
    rect(d,(18,94,522,184),20,(9,10,35,228),(251,47,139,250),2)
    write(d,(35,108),title,25,highlight)
    write(d,(35,149),subtitle,13,COLOR["white"])
    if segment in (0,1,2):
      # Phone arrives with inertia; scene content changes with presenter.
      e=ease(min(1,(t-segment*total/4)/.45))
      ph=phone(t,segment)
      x=271+int((1-e)*320+12*math.sin(1.7*t));y=365+int(4*math.sin(t*1.1))
      overlay.alpha_composite(ph,(x,y))
      if segment>0:
        rect(d,(278,770,523,824),12,(186,24,69,226),(255,224,80,255),2)
        write(d,(295,785),"POSSÍVEL GOLPE!",17,COLOR["white"])
    rect(d,(19,870,522,930),16,(9,14,39,234),(251,47,139,255),2)
    write(d,(35,887),"SALVE   •   COMPARTILHE   •   SIGA",16,COLOR["white"])
    rect(d,(23,945,516,953),4,(51,63,91,255))
    rect(d,(23,945,23+int((493)*min(1,t/total)),953),4,(251,47,139,255))
    img=Image.fromarray(base).convert("RGBA");img.alpha_composite(overlay)
    return img.convert("RGB")

def main():
    master=read_image(A);alert=read_image(B)
    with tempfile.TemporaryDirectory() as d:
        tmp=Path(d);voice=tmp/"voice.mp3";script=speech(voice)
        duration=float(info(voice)["format"]["duration"])+.45
        out=OUTPUT/"piloto_personagem_cinematica.mp4"
        command=["ffmpeg","-y","-loglevel","error",
                 "-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}",
                 "-framerate",str(RENDER_FPS),"-i","pipe:0",
                 "-i",str(voice),"-map","0:v:0","-map","1:a:0",
                 "-t",f"{duration:.3f}","-vf","fps=30,scale=720:1280:flags=lanczos,format=yuv420p",
                 "-c:v","libx264","-preset","veryfast","-crf","25",
                 "-c:a","aac","-b:a","128k","-movflags","+faststart",str(out)]
        process=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for i in range(math.ceil(duration*RENDER_FPS)):
                process.stdin.write(draw_scene(i/RENDER_FPS,duration,master,alert).tobytes())
        except BrokenPipeError as exc:raise RuntimeError("FFmpeg falhou durante renderização") from exc
        finally:process.stdin.close()
        if process.wait()!=0:raise RuntimeError("FFmpeg não produziu vídeo válido")
        meta=info(out)
        vid=next((x for x in meta["streams"] if x["codec_type"]=="video"),{})
        aud=next((x for x in meta["streams"] if x["codec_type"]=="audio"),{})
        if not (vid.get("width")==720 and vid.get("height")==1280
                and vid.get("codec_name")=="h264" and aud.get("codec_name")=="aac"
                and float(meta["format"]["duration"])>9):
            raise RuntimeError("Piloto não passou validação técnica")
        data={"title":"Pix urgente — piloto visual da personagem feminina",
              "visual_format":"PERSONAGEM_CGI_2_5D_V1","rigged_3d":False,
              "user_approved":False,"published":False,"auto_publish":False,
              "voice_engine":"Edge TTS pt-BR Francisca","duration_s":round(duration,1),
              "script":script,"status":"review_only",
              "source_images":["public/assets/personagem-mestre.jpg","public/assets/personagem-pix-alerta.jpg"],
              "note":"Imagens CGI em 2.5D com telas animadas; NÃO confundir com animação 3D completa."}
        (OUTPUT/"piloto_personagem_cinematica.json").write_text(
            json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print("PILOTO VALIDADO",out,round(duration,1),out.stat().st_size,flush=True)

if __name__=="__main__":main()
