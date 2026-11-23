#!/usr/bin/env python3
"""Pilotos híbridos 03 (permissões) e 04 (backup).
Reutiliza motor e personagem CGI; demonstrações específicas em celular.
Nunca envia ao TikTok nem ao Metricool.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,subprocess,tempfile
import hibrido_02_senhas as base

W,H,FPS=base.W,base.H,base.FPS
WHITE,PINK,CYAN,YELLOW,GREEN,RED,NAVY=(base.WHITE,base.PINK,base.CYAN,base.YELLOW,
                                         base.GREEN,base.RED,base.NAVY)
SCRIPT={
"permissoes":{
"art":"personagem-permissoes.jpg","slug":"hibrido_03_permissoes_celular",
"footer":"PERMISSÃO SÓ QUANDO PRECISAR",
"scenes":[
("ATENÇÃO","SEU CELULAR TE OBSERVA?","Veja quais acessos você liberou",
 "Você já conferiu quais aplicativos podem usar sua câmera, microfone e localização? Algumas permissões podem ficar ativas sem necessidade.","hook"),
("ABRA OS AJUSTES","PERMISSÕES DO CELULAR","O controle está nas configurações",
 "No seu celular, entre em Configurações e procure por aplicativos e permissões. O nome do menu pode mudar conforme o aparelho.","settings"),
("LOCALIZAÇÃO","QUEM SABE ONDE VOCÊ ESTÁ?","Revise o acesso à localização",
 "Um aplicativo de mapa pode precisar da sua localização para orientar o caminho. Mas isso não significa que precise acessá-la sempre.","location"),
("CÂMERA","QUEM PODE ABRIR A CÂMERA?","Permissão precisa ter motivo",
 "Aplicativos que tiram fotos ou fazem chamadas de vídeo precisam da câmera. Outros podem não ter um motivo claro para pedir acesso.","camera"),
("MICROFONE","REVISE O MICROFONE","Ative somente quando necessário",
 "O mesmo vale para o microfone. Se você não usa uma função que grava áudio, avalie retirar essa permissão do aplicativo.","microphone"),
("ACESSO CONTROLADO","SÓ DURANTE O USO","Evite acesso permanente sem motivo",
 "Quando existir a opção, escolha permitir somente durante o uso do aplicativo. Isso reduz acessos desnecessários em segundo plano.","toggle"),
("NEGUE QUANDO PUDER","NÃO PRECISA? NÃO LIBERE","Alguns recursos podem parar",
 "Se a permissão não é necessária para a função desejada, você pode negar. Algumas funções específicas podem deixar de funcionar.","revoke"),
("PRAZER, PRIVACIDADE","CONFIRA APP POR APP","Reavalie após instalar um aplicativo",
 "Uma revisão rápida de tempos em tempos ajuda a perceber aplicativos com permissões que você nem lembrava ter autorizado.","review"),
("TRÊS PASSOS","VERIFIQUE ANTES DE AUTORIZAR","Localização, câmera e microfone",
 "Antes de tocar em permitir, pergunte: por que esse aplicativo precisa disso, por quanto tempo e o que acontece se eu negar?","recap"),
("FECHAMENTO","CONTROLE SUA PRIVACIDADE","Salve para revisar depois",
 "Salve este vídeo e mande para alguém que usa o celular todos os dias. Uma conferida nas permissões faz diferença.","cta")
]},
"backup":{
"art":"personagem-backup.jpg","slug":"hibrido_04_backup_fotos",
"footer":"SUAS FOTOS MERECEM BACKUP",
"scenes":[
("IMPORTANTE","E SE O CELULAR QUEBRAR?","Suas fotos podem sumir",
 "E se seu celular parar de funcionar hoje? Você conseguiria recuperar suas fotos e vídeos mais importantes?","hook"),
("RISCO REAL","FOTOS SÓ NO APARELHO?","A memória do celular não é backup",
 "Guardar fotos apenas na memória do celular pode ser arriscado. Uma queda, perda ou defeito pode levar seus arquivos embora.","gallery"),
("CÓPIA DE SEGURANÇA","FAÇA BACKUP","Uma segunda cópia em local seguro",
 "Backup é ter uma segunda cópia dos arquivos em outro lugar seguro, como um serviço de nuvem ou armazenamento externo.","cloud"),
("NÃO É MÁGICA","ESCOLHA ONDE GUARDAR","Entenda espaço e privacidade",
 "Antes de ativar o backup, verifique o espaço disponível, as condições do serviço e como ele protege seus dados.","storage"),
("AUTOMATIZE","ATIVE O BACKUP AUTOMÁTICO","Se o aplicativo oferecer",
 "Se o serviço oferecer essa opção, ative cópias automáticas. Assim, você não depende de lembrar de salvar tudo manualmente.","auto"),
("USE WI-FI","CUIDE DA SUA INTERNET","Transferências podem ser grandes",
 "Suas fotos e vídeos podem ocupar bastante espaço. Se preferir, configure o envio por Wi-Fi para poupar dados móveis.","wifi"),
("CONFIRA","NÃO BASTA ATIVAR","Verifique se terminou de enviar",
 "Depois de configurar, confira se as fotos realmente apareceram na cópia de segurança. Um backup incompleto pode dar falsa tranquilidade.","verify"),
("PROTEÇÃO EXTRA","SEGURE SUA CONTA","Senha forte e duas etapas",
 "Proteja a conta usada para guardar fotos com senha exclusiva e autenticação em duas etapas, quando estiver disponível.","protect"),
("TESTE DE RECUPERAÇÃO","VOCÊ CONSEGUE RESTAURAR?","Uma cópia boa pode ser recuperada",
 "De vez em quando, confira se consegue visualizar e recuperar um arquivo da cópia. Isso ajuda a identificar problemas antes de precisar.","restore"),
("FINAL","NÃO PERCA SUAS MEMÓRIAS","Salve esta dica útil",
 "Você tem fotos importantes no celular? Salva esta dica e compartilha com alguém da família para ninguém perder lembranças.","cta")
]}}
def rr(d,xy,r,fill,outline=None,w=1):
    base.rr(d,xy,r,fill,outline,w)
def txt(d,xy,s,size=20,color=WHITE):
    base.txt(d,xy,s,size,color)
def phone(d):
    return base.phone(d,70,206,400,595)
def pill(d,xy,s,bg,color=WHITE,size=17):
    base.pill(d,xy,s,bg,color,size)
def check(d,x,y,is_on=True):
    rr(d,(x,y,x+86,y+46),22,GREEN if is_on else (67,70,104))
    cx=x+60 if is_on else x+25
    d.ellipse((cx-15,y+8,cx+15,y+38),fill=(242,248,255))
def cell_perms(im,kind,local,dt,t):
    d=ImageDraw.Draw(im)
    p=min(1,local/max(.1,dt))
    phase=int(p*4)
    if kind in ("settings","review","location","camera","microphone","toggle","revoke"):
        x,y,w,h=phone(d)
        txt(d,(x+35,y+70),"PERMISSÕES",24)
        rows=[("LOCALIZAÇÃO","📍"),("CÂMERA","●"),("MICROFONE","◉")]
        for i,(label,icon) in enumerate(rows):
            yy=y+155+i*121
            rr(d,(x+30,yy,x+w-30,yy+100),16,(33,39,78),(85,102,164),2)
            txt(d,(x+48,yy+17),label,19)
            active=(kind=="toggle" and phase<i) or (kind=="revoke" and phase<i)
            if kind in ("location","camera","microphone"):
                active=label.lower()!=kind and phase<2
            check(d,x+w-146,yy+49,active)
        target=min(2,phase)
        base.action_pulse(d,x+w-103,y+155+target*121+72,t,
                          RED if kind=="revoke" else CYAN)
        if kind in ("toggle","revoke","location","camera","microphone"):
            pill(d,(x+44,y+537),"REVOGAR SE NÃO PRECISA",(96,29,77),WHITE,15)
        return
    if kind in ("recap",):
        for i,title in enumerate(("LOCALIZAÇÃO","CÂMERA","MICROFONE")):
            yy=250+i*151
            rr(d,(54,yy,486,yy+109),18,(27,41,76),CYAN if phase>=i else (86,81,139),3)
            rr(d,(72,yy+27,122,yy+80),14,PINK)
            txt(d,(88,yy+39),str(i+1),22)
            txt(d,(147,yy+40),title,21)
        return
    rr(d,(26,575,515,720),23,(18,23,58),(252,61,152),3)
    txt(d,(52,607),"PRIVACIDADE IMPORTA",22,YELLOW)
    txt(d,(52,656),"REVISE OS ACESSOS",20,CYAN)

def cell_backup(im,kind,local,dt,t):
    d=ImageDraw.Draw(im)
    p=min(1,local/max(.1,dt))
    phase=int(p*4)
    if kind in ("gallery","cloud","storage","auto","wifi","verify","restore","protect"):
        x,y,w,h=phone(d)
        title="FOTOS E VÍDEOS" if kind in ("gallery","restore") else "CÓPIA DE SEGURANÇA"
        txt(d,(x+28,y+58),title,21)
        colors=[(255,122,156),(107,155,242),(83,203,172),(255,197,103),(194,127,239),(104,183,216)]
        for i,col in enumerate(colors):
            sx=x+35+(i%3)*107;sy=y+140+(i//3)*123
            rr(d,(sx,sy,sx+96,sy+108),15,col,(228,235,250),2)
            d.ellipse((sx+59,sy+13,sx+78,sy+31),fill=YELLOW)
            d.polygon([(sx+10,sy+88),(sx+39,sy+47),(sx+61,sy+74),(sx+85,sy+36),(sx+88,sy+94)],fill=(34,65,82))
            if kind=="gallery" and phase>=i//2:
                rr(d,(sx+4,sy+4,sx+92,sy+104),10,(20,22,43,170))
        selected=min(5,phase+1)
        sx=x+35+(selected%3)*107;sy=y+140+(selected//3)*123
        base.action_pulse(d,sx+48,sy+54,t,GREEN)
        if kind=="cloud":
            rr(d,(x+64,y+407,x+w-64,y+471),22,(36,89,140),CYAN,3)
            txt(d,(x+92,y+421),"↑  BACKUP",19)
        elif kind in ("auto","wifi","storage"):
            rr(d,(x+32,y+415,x+w-32,y+483),17,(31,41,80),(78,104,158),2)
            txt(d,(x+45,y+432),"AUTOMÁTICO" if kind=="auto" else "SÓ WI-FI" if kind=="wifi" else "ESPAÇO LIVRE",17)
            check(d,x+w-156,y+428,phase>=1)
        else:
            bar=round(310*(.08+.92*p))
            rr(d,(x+41,y+445,x+w-41,y+468),12,(51,64,107))
            rr(d,(x+41,y+445,x+41+bar,y+468),12,GREEN)
            txt(d,(x+50,y+498),"CÓPIA CONFERIDA" if kind in ("verify","restore") else "SENHA FORTE",17,GREEN)
        return
    if kind=="recap":
        for i,s in enumerate(("CÓPIA EM OUTRO LUGAR","BACKUP AUTOMÁTICO","CONFIRA SE FUNCIONA")):
            yy=248+i*155
            rr(d,(52,yy,488,yy+105),17,(29,37,75),CYAN if phase>=i else (80,85,137),3)
            rr(d,(73,yy+22,124,yy+83),14,PINK)
            txt(d,(90,yy+36),str(i+1),22)
            txt(d,(142,yy+36),s,17)
        return
    rr(d,(25,570,515,712),22,(14,22,54),PINK,3)
    txt(d,(47,593),"SUAS FOTOS SÃO ÚNICAS",21,YELLOW)
    txt(d,(47,644),"FAÇA UMA CÓPIA",22,CYAN)

def picture(t,lens,bounds,master,theme,scenes,render):
    import math
    idx=next((k for k in range(len(lens)) if bounds[k]<=t<bounds[k+1]),len(lens)-1)
    _,title,sub,spoken,kind=scenes[idx]
    local=t-bounds[idx];dt=lens[idx]
    is_hero=kind in ("hook","cta")
    image=base.background(t,is_hero,master)
    if not is_hero:
        image=Image.blend(image,Image.new("RGB",(W,H),NAVY),.65)
    d=ImageDraw.Draw(image)
    for k in range(11):
        x=(k*67+int(t*6))%W; y=(k*139+int(t*15))%H
        d.ellipse((x-2,y-2,x+2,y+2),fill=CYAN if k%2 else PINK)
    rr(d,(18,20,522,77),14,(10,14,36),PINK,2)
    txt(d,(34,33),"METON DIGITAL",23)
    txt(d,(408,42),"100% IA",14,PINK)
    if not is_hero:
        rr(d,(19,91,522,177),15,(17,16,48),(93,94,151),2)
        txt(d,(35,102),title,24,CYAN if kind!="revoke" else YELLOW)
        txt(d,(36,144),sub,14)
    render(image,kind,local,dt,t)
    d=ImageDraw.Draw(image)
    caption=base.short_caption(spoken,local,dt)
    rr(d,(20,778,520,838),15,(6,10,29),PINK,2)
    txt(d,(35,793),caption[:43],16,WHITE)
    rr(d,(20,852,520,909),15,(9,14,37),CYAN,2)
    footer="SALVE  •  COMPARTILHE  •  SIGA" if idx>=len(scenes)-2 else SCRIPT[theme]["footer"]
    txt(d,(32,868),footer,17)
    rr(d,(24,927,516,936),4,(59,67,111))
    rr(d,(24,927,24+int(492*min(1,t/bounds[-1])),936),4,PINK)
    return image

def generate(theme):
    specs=SCRIPT[theme]
    scenes=specs["scenes"]
    master=base.img_source(base.ASSET/"personagem-mestre.jpg")
    show=specs.get("renderer") or (cell_perms if theme=="permissoes" else cell_backup)
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        audios=[]
        durations=[]
        for i,(_,_,_,speech,_) in enumerate(scenes):
            p=tmp/f"narracao_{i:02d}.mp3"
            base.run(["edge-tts","--voice","pt-BR-FranciscaNeural","--rate=-10%",
                "--text",speech,"--write-media",str(p)])
            seconds=float(base.probe(p)["format"]["duration"])
            if seconds<3: raise RuntimeError("Narração curta "+theme)
            audios.append(p);durations.append(seconds)
        plist=tmp/"lista.ffconcat"
        plist.write_text("ffconcat version 1.0\n"+"\n".join("file '"+str(x)+"'" for x in audios)+"\n",encoding="utf8")
        audio=tmp/"audio.mp3"
        base.run(["ffmpeg","-y","-loglevel","error","-safe","0","-f","concat","-i",str(plist),
            "-c:a","libmp3lame","-b:a","128k",str(audio)])
        total=float(base.probe(audio)["format"]["duration"])
        if total<56: raise RuntimeError("Episódio muito curto para revisão: "+str(total))
        bounds=[0.]
        for n in durations:bounds.append(bounds[-1]+n)
        target=base.OUT/(specs["slug"]+".mp4")
        cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24",
            "-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-i",str(audio),
            "-t",f"{total:.3f}","-vf","fps=30,scale=720:1280:flags=lanczos,format=yuv420p",
            "-c:v","libx264","-preset","veryfast","-crf","25","-c:a","aac",
            "-b:a","128k","-movflags","+faststart",str(target)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for n in range(math.ceil(total*FPS)):
                proc.stdin.write(picture(n/FPS,durations,bounds,master,theme,scenes,show).tobytes())
        except BrokenPipeError as exc:raise RuntimeError("Erro FFmpeg "+theme) from exc
        finally:proc.stdin.close()
        if proc.wait()!=0:raise RuntimeError("Falha na renderização "+theme)
        stats=base.probe(target)
        v=next(x for x in stats["streams"] if x["codec_type"]=="video")
        a=next(x for x in stats["streams"] if x["codec_type"]=="audio")
        assert v["codec_name"]=="h264" and v["width"]==720 and v["height"]==1280 and a["codec_name"]=="aac"
        info={"title":"Permissões do celular" if theme=="permissoes" else "Backup das fotos",
          "profile":"@metonalencar","format":"720x1280 H264 AAC 30fps",
          "visual_style":"HÍBRIDO CGI + CELULAR ANIMADO",
          "duration_s":round(float(stats["format"]["duration"]),1),"scene_count":len(scenes),
          "narration":"pt-BR-FranciscaNeural","approved":False,"published":False,
          "scheduled":False,"status":"review_only"}
        (base.OUT/(specs["slug"]+".json")).write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n")
        print("HIBRIDO_OK",theme,info,flush=True)

if __name__=="__main__":
    for topic in ("permissoes","backup"):
        generate(topic)
