#!/usr/bin/env python3
"""Piloto híbrido 01: golpe do Pix urgente.
Usa o mesmo motor dos vídeos 02/03/04 e interface do celular
específica do Pix. NÃO publica automaticamente.

Revisão 24/11: planos CGI narrativos e legendas sem corte de palavras.
"""
import json, math
from PIL import Image,ImageDraw
import hibrido_03_04 as engine
import hibrido_02_senhas as base
W,H=base.W,base.H
PINK,CYAN,YELLOW,GREEN,RED,WHITE,NAVY=(base.PINK,base.CYAN,base.YELLOW,base.GREEN,
                                        base.RED,base.WHITE,base.NAVY)
STORY=[
 ("GANCHO","PEDIDO DE PIX URGENTE?","Pare antes de transferir",
 "Chegou uma mensagem pedindo um Pix urgente de alguém conhecido? Antes de pagar, olha esta situação. Pode ser um golpe.","hook"),
 ("O PEDIDO","AMIGA, PRECISO AGORA!","A pressão começa na mensagem",
 "O contato diz que está passando por uma emergência e precisa do dinheiro imediatamente. A pressa tenta impedir que você confira os detalhes.","chat"),
 ("DESCONFIE","NOME E FOTO NÃO BASTAM","Um perfil pode ser imitado",
 "Ver a foto e o nome de um amigo na conversa não garante que o pedido veio mesmo dessa pessoa.","profile"),
 ("O RISCO","NÃO FAÇA PIX NA PRESSA","Evite transferir sem confirmar",
 "Quando a mensagem começa a pressionar, não finalize o pagamento. Uma transferência enviada ao destinatário errado pode ser difícil de recuperar.","transfer"),
 ("PARE AGORA","INTERROMPA O PAGAMENTO","Atenção aos sinais",
 "Se o pedido for inesperado, especialmente com urgência e histórias confusas, faça uma pausa. Você não precisa decidir naquele instante.","stop"),
 ("CONFIRME","LIGUE PARA O CONTATO SALVO","Faça a verificação por outro caminho",
 "Pegue o número que já estava salvo no seu celular e ligue para a pessoa. Não confie em números enviados na mensagem suspeita.","call"),
 ("OUTRO CANAL","NÃO USE O NÚMERO ENVIADO","Evite confirmar no mesmo chat",
 "Se não conseguir falar por telefone, tente outro meio conhecido. O importante é confirmar a identidade de forma independente.","compare"),
 ("RESULTADO","SUSPEITA CONFIRMADA?","Avise e proteja seus contatos",
 "Se a pessoa disser que nunca pediu dinheiro, avise que alguém pode estar usando o nome dela para tentar enganar outras pessoas.","resolve"),
 ("RESUMO","TRÊS PASSOS","Pare, ligue e confirme",
 "Guarde estes três passos: pare, ligue para o número que você já conhece e só considere pagar depois de confirmar o pedido.","recap"),
 ("ENCERRAMENTO","PROTEJA SUA FAMÍLIA","Salve e compartilhe",
 "Esse aviso pode evitar um prejuízo. Salve o vídeo e compartilhe com alguém que precisa conhecer esse golpe.","cta")
]
engine.SCRIPT["pix"]={"slug":"hibrido_01_pix_urgente","footer":"PIX URGENTE? PARE E CONFIRME",
                       "title":"Golpe do Pix urgente","scenes":STORY,
                       "art_by_kind":{
                         "hook":"personagem-pix-alerta.jpg",
                         "stop":"personagem-bloqueio.jpg",
                         "call":"personagem-ligacao.jpg",
                         "resolve":"personagem-resolucao.jpg",
                         "cta":"personagem-mestre.jpg"
                       }}

def cell_pix(im,kind,local,dt,t):
    rr=base.rr
    d=ImageDraw.Draw(im)
    if kind in ('hook','cta'):
        rr(d,(28,590,510,716),20,(16,20,58),PINK,3)
        base.txt(d,(48,610),'PIX URGENTE?',26,YELLOW)
        base.txt(d,(48,656),'PARE E CONFIRME!' if kind=='hook' else 'SALVE E COMPARTILHE',19,CYAN)
        return
    x,y,w,h=base.phone(d,70,202,400,586)
    phase=int(max(0,min(1,local/max(.1,dt)))*4)
    if kind in ("chat","profile","transfer","stop","compare"):
        base.txt(d,(x+34,y+64),"MENSAGENS" if kind in ("chat","profile","compare") else "CONFIRMAR PIX",21)
        if kind in ("chat","profile","compare"):
            rr(d,(x+35,y+136,x+w-35,y+187),15,(40,50,91),(93,110,164),2)
            base.txt(d,(x+51,y+149),"CONTATO CONHECIDO",16)
            bubbles=[
                ("OI, ME AJUDA?",(46,53,96),0),
                ("PRECISO DE UM PIX!",(110,34,82),1),
                ("É URGENTE AGORA",(125,31,67),2)
            ]
            for j,(msg,color,level) in enumerate(bubbles):
                yy=y+212+j*83
                if phase>=level:
                    rr(d,(x+35,yy,x+w-35,yy+66),16,color)
                    base.txt(d,(x+48,yy+18),msg,18,YELLOW if j else WHITE)
            if kind=="profile":
                rr(d,(x+40,y+499,x+w-40,y+555),13,(147,33,69),RED,2)
                base.txt(d,(x+66,y+516),"CONFIRA A IDENTIDADE",17)
            if kind=="compare":
                rr(d,(x+45,y+501,x+w-45,y+555),14,(31,118,103),GREEN,2)
                base.txt(d,(x+67,y+516),"USE OUTRO CANAL",17,NAVY)
            target_y=y+244+min(2,phase)*83
            base.action_pulse(d,x+w-55,target_y,t,RED if phase>=1 else CYAN)
        else:
            rr(d,(x+42,y+145,x+w-42,y+224),17,(31,46,81),(86,110,146),2)
            base.txt(d,(x+64,y+163),"VALOR DO PIX",17)
            base.txt(d,(x+66,y+196),"R$ 500,00",23,YELLOW)
            rr(d,(x+42,y+275,x+w-42,y+341),14,(29,39,77))
            base.txt(d,(x+60,y+296),"CONFERIR DESTINATÁRIO",15)
            if kind=="stop":
                rr(d,(x+29,y+404,x+w-29,y+527),20,(154,27,63),RED,3)
                base.txt(d,(x+102,y+436),"PARE!",35,YELLOW)
                base.action_pulse(d,x+w//2,y+466,t,RED)
            else:
                rr(d,(x+30,y+437,x+w-30,y+501),17,(40,72,81),(59,214,202),3)
                base.txt(d,(x+93,y+453),"NÃO CONFIRMAR",20)
        return
    if kind=="call":
        base.txt(d,(x+96,y+94),"LIGANDO...",23,CYAN)
        d.ellipse((x+126,y+186,x+274,y+334),fill=(47,64,109),outline=CYAN,width=4)
        base.txt(d,(x+167,y+219),"✓",52,GREEN)
        base.txt(d,(x+83,y+365),"CONTATO JÁ SALVO",18)
        d.ellipse((x+131,y+445,x+258,y+572),fill=GREEN)
        base.txt(d,(x+169,y+478),"☎",39,NAVY)
        base.action_pulse(d,x+194,y+508,t,GREEN)
        return
    if kind=="resolve":
        base.txt(d,(x+100,y+86),"CONFIRMADO!",23,GREEN)
        base.rr(d,(x+49,y+205,x+w-49,y+320),19,(24,92,94),CYAN,3)
        base.txt(d,(x+81,y+224),"NÃO FUI EU!",25,YELLOW)
        base.txt(d,(x+90,y+271),"PEDIDO SUSPEITO",17)
        base.rr(d,(x+57,y+380,x+w-57,y+480),18,(28,62,77),GREEN,2)
        base.txt(d,(x+88,y+404),"AVISE CONTATOS",17)
        return
    if kind=="recap":
        for i,title in enumerate(("PARE","LIGUE","CONFIRME")):
            yy=y+141+i*141
            base.rr(d,(x+32,yy,x+w-32,yy+113),17,(29,38,83),CYAN if phase>=i else (83,93,144),3)
            base.rr(d,(x+48,yy+29,x+100,yy+80),14,PINK)
            base.txt(d,(x+62,yy+38),str(i+1),23)
            base.txt(d,(x+132,yy+37),title,26)
        return
    # Hero image with alert in action
    base.rr(d,(x-30,y+286,x+w+30,y+420),22,(17,21,58),PINK,3)
    base.txt(d,(x,y+313),"PIX URGENTE?",28,YELLOW)
    base.txt(d,(x,y+362),"LIGUE ANTES!",24,CYAN)
engine.SCRIPT["pix"]["renderer"]=cell_pix

if __name__=="__main__":
    engine.generate("pix")
    meta_path=base.OUT/"hibrido_01_pix_urgente.json"
    meta=json.loads(meta_path.read_text(encoding="utf8"))
    meta["title"]="Golpe do Pix urgente"
    meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("PIX_HIBRIDO_COMPLETO",meta,flush=True)

# Render revision 2026-11-23: ações e legendas dinâmicas.
