#!/usr/bin/env python3
"""Piloto narrativo >60s de PIX com 3D CGI ilustrado e movimentos 2.5D.
SEM POSTAGEM AUTOMATICA. Requer aprovação visual depois da revisão do MP4 real.
Executar: python scripts/piloto_pix_completo.py
"""
import json, math, subprocess, tempfile
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from piloto_visual_personagem import (ROOT, ASSETS, OUTPUT, W, H, RENDER_FPS, COLOR,
      read_image, run, info, rect, write, ease, mouth_motion, phone)

STORY=[
 ("mestre","PEDIDO DE PIX?","PARE ANTES DE PAGAR",
  "Recebeu uma mensagem pedindo um Pix urgente? Não faça a transferência imediatamente. Pode ser alguém tentando enganar você.",
  "warning"),
 ("pix-alerta","MENSAGEM URGENTE","CUIDADO COM A PRESSA",
  "A pessoa diz que teve uma emergência e precisa receber agora. Essa pressa é uma das principais estratégias dos golpistas.",
  "chat"),
 ("pix-alerta","FOTO CONHECIDA","NÃO COMPROVA IDENTIDADE",
  "Mesmo quando a foto e o nome parecem familiares, você ainda precisa confirmar se realmente está conversando com aquela pessoa.",
  "chat"),
 ("bloqueio","NÃO TRANSFIRA","INTERROMPA O PAGAMENTO",
  "Se um contato pedir dinheiro de repente, pare. Não digite a senha do banco nem confirme nenhum Pix sob pressão.",
  "warning"),
 ("ligacao","USE OUTRO CANAL","LIGUE PARA CONFIRMAR",
  "Abra os contatos do seu próprio celular e ligue para o número antigo que você já tinha salvo daquela pessoa.",
  "call"),
 ("ligacao","NÚMERO CONHECIDO","NADA DE CONTATO NOVO",
  "Não use números desconhecidos enviados na conversa suspeita. A confirmação precisa acontecer fora daquela mesma troca de mensagens.",
  "call"),
 ("resolucao","CONFIRMAÇÃO REAL","CONFIRA ANTES DO PIX",
  "Pergunte diretamente se o pedido de dinheiro é verdadeiro. Se a pessoa negar, você provavelmente evitou um golpe.",
  "ok"),
 ("bloqueio","PROTEJA SEU ACESSO","NÃO ENVIE CÓDIGOS",
  "Nunca compartilhe códigos enviados por mensagem nem senhas bancárias. Eles podem permitir acesso indevido às suas contas.",
  "warning"),
 ("senhas","SEGURANÇA EXTRA","USE VERIFICAÇÃO EM DUAS ETAPAS",
  "Proteja suas contas com autenticação adicional e atualize os meios de recuperação. Isso aumenta sua segurança em diferentes situações.",
  "lock"),
 ("resolucao","CONVERSE EM FAMÍLIA","UM CUIDADO EVITA PREJUÍZO",
  "Combine com seus familiares que pedidos urgentes de dinheiro serão confirmados por uma ligação antes de qualquer transferência.",
  "ok"),
 ("mestre","GUARDE ESSA DICA","PARE. LIGUE. CONFIRME.",
  "Lembre sempre: uma mensagem convincente não comprova identidade. Salve este vídeo, compartilhe e acompanhe mais dicas digitais.",
  "cta"),
]

def voice_parts(tmp):
    tracks=[];duration=[]
    for idx,(_,_,_,text,_) in enumerate(STORY):
        mp3=tmp/f"fala_{idx:02d}.mp3"
        run(["edge-tts","--voice","pt-BR-FranciscaNeural",
             "--rate=-6%","--text",text,"--write-media",str(mp3)],timeout=150)
        d=float(info(mp3)["format"]["duration"])
        if d<2:raise RuntimeError("Trecho de voz inválido "+str(idx))
        tracks.append(mp3);duration.append(d)
    playlist=tmp/"voices.ffconcat"
    playlist.write_text("ffconcat version 1.0\n"+"\n".join("file '"+str(x)+"'" for x in tracks)+"\n",encoding="utf8")
    combined=tmp/"narracao.mp3"
    run(["ffmpeg","-y","-loglevel","error","-safe","0","-f","concat",
         "-i",str(playlist),"-c:a","libmp3lame","-b:a","128k",str(combined)])
    return combined,duration

def add_phone(layer,t,mode,local):
    d=ImageDraw.Draw(layer)
    if mode in ("chat","warning","call"):
        ph=phone(t,0)
        progress=ease(local/.60)
        x=278+int((1-progress)*300+6*math.sin(t))
        y=373+int(7*math.cos(t*.9))
        layer.alpha_composite(ph,(x,y))
    if mode=="warning":
        rect(d,(280,765,522,815),15,(180,24,59,233),(255,217,50,255),2)
        write(d,(299,775),"ATENÇÃO AO PIX!",16,COLOR["white"])
    elif mode=="call":
        rect(d,(280,765,522,815),15,(15,116,73,235),(79,250,183,255),2)
        write(d,(297,777),"LIGUE PARA SALVO",14,COLOR["white"])
    elif mode=="lock":
        rect(d,(270,725,520,813),16,(15,21,64,232),(64,231,241,255),3)
        write(d,(293,748),"DUAS ETAPAS",17,COLOR["cyan"])
    elif mode=="ok":
        rect(d,(270,746,522,810),15,(19,119,78,236),(75,251,188,255),3)
        write(d,(290,763),"CONFIRMADO!",18,COLOR["white"])

def frame(t,parts,bounds,images):
    ix=max(0,min(len(STORY)-1,next((k for k in range(len(bounds)-1) if bounds[k]<=t<bounds[k+1]),len(STORY)-1)))
    local=t-bounds[ix];dt=bounds[ix+1]-bounds[ix]
    key,heading,subtitle,spoken,mode=STORY[ix]
    # Alternate framing within each scene: cinematic micro-cut around midpoint.
    mid=local>dt*.52
    source=images[key]
    angle=math.sin(t*1.2)*.45
    zoom=1.019 + (0.014 if mid else 0) + .006*math.sin(t*.67)
    mat=cv2.getRotationMatrix2D((W*.50,H*.39),angle,zoom)
    mat[0,2]+=5*math.sin(t*.71)+(5 if mid else -4)
    mat[1,2]+=4*math.cos(t*.91)
    bg=cv2.warpAffine(source,mat,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    if key=="mestre": bg=mouth_motion(bg,t)
    layer=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(layer)
    rect(d,(16,25,524,71),14,(10,12,33,235),(248,42,141,255),2)
    write(d,(32,37),"@METONALENCAR  •  DICAS DIGITAIS",18,COLOR["white"])
    rect(d,(16,95,524,187),20,(10,12,38,236),(248,45,142,255),2)
    accent=COLOR["red"] if mode=="warning" else COLOR["cyan"] if mode in ("lock","call") else COLOR["yellow"] if mode=="chat" else COLOR["white"]
    write(d,(31,111),heading,25,accent)
    write(d,(31,152),subtitle,14,COLOR["white"])
    add_phone(layer,t,mode,local)
    rect(d,(20,872,520,932),15,(10,13,37,237),(249,44,139,255),2)
    if ix<len(STORY)-1:footer="SEGURANÇA DIGITAL  •  ENTENDA O GOLPE"
    else:footer="SALVE  •  COMPARTILHE  •  SIGA"
    write(d,(31,889),footer,15,COLOR["white"])
    rect(d,(22,946,518,953),3,(51,63,85,255))
    rect(d,(22,946,22+int(496*min(1,t/bounds[-1])),953),3,(255,50,146,255))
    img=Image.fromarray(bg).convert("RGBA");img.alpha_composite(layer)
    return img.convert("RGB")

def main():
    names=set(x[0] for x in STORY)
    images={name:read_image(ASSETS/("personagem-"+name+".jpg")) for name in names}
    with tempfile.TemporaryDirectory() as d:
        tmp=Path(d);narration,durations=voice_parts(tmp)
        bounds=[0.]
        for secs in durations:bounds.append(bounds[-1]+secs)
        duration=float(info(narration)["format"]["duration"])
        if duration<61:
            raise RuntimeError("Roteiro narrado abaixo de 61s: "+str(duration))
        out=OUTPUT/"piloto_pix_completo_3d_visual.mp4"
        command=["ffmpeg","-y","-loglevel","error","-f","rawvideo",
        "-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(RENDER_FPS),"-i","pipe:0",
        "-i",str(narration),"-map","0:v:0","-map","1:a:0",
        "-t",f"{duration:.3f}","-vf","fps=30,scale=720:1280:flags=lanczos,format=yuv420p",
        "-c:v","libx264","-preset","veryfast","-crf","26",
        "-c:a","aac","-b:a","128k","-movflags","+faststart",str(out)]
        process=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for i in range(math.ceil(duration*RENDER_FPS)):
                process.stdin.write(frame(i/RENDER_FPS,durations,bounds,images).tobytes())
        except BrokenPipeError as exc:raise RuntimeError("Falha FFmpeg") from exc
        finally:process.stdin.close()
        if process.wait()!=0:raise RuntimeError("Falha no arquivo final")
        data=info(out)
        v=next(x for x in data["streams"] if x["codec_type"]=="video")
        a=next(x for x in data["streams"] if x["codec_type"]=="audio")
        actual=float(data["format"]["duration"])
        if not (v["width"]==720 and v["height"]==1280 and v["codec_name"]=="h264" and a["codec_name"]=="aac" and actual>61):
            raise RuntimeError("MP4 não passou verificação técnica")
        obj={"title":"O golpe do Pix urgente — piloto de episódio completo","date_created":"2026-11-08",
            "duration_s":round(actual,1),"scenes":len(STORY),"image_assets":len(names),
            "voice":"Edge TTS pt-BR Francisca","format":"720x1280 H264 AAC",
            "visual_type":"CGI 2.5D com cenas e UI animada; não malha 3D",
            "quality_review_required":True,"approved":False,
            "autoPublish":False,"published":False,
            "status":"review_only"}
        (OUTPUT/"piloto_pix_completo_3d_visual.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print("PILOTO COMPLETO VALIDADO",out,round(actual,1),"s",out.stat().st_size,flush=True)

if __name__=="__main__":main()
