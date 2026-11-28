#!/usr/bin/env python3
"""Barreira técnica para retorno seguro do TikTok IA.

NÃO PUBLICA, NÃO PUBLICA NO METRICOOL E NÃO SUBSTITUI REVISÃO CRIATIVA.
Entrada: public/release-candidates/semana-atual.json (somente após vídeos terminados).
Cada entrada precisa de um MP4 real e evidências da inspeção visual.
"""
import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/"public/release-candidates/semana-atual.json"
OLD_MARKERS=("B+ NEXO","STORY 2D CENAS HUMANAS","SLIDES","TEMPLATE ESTATICO",
             "PERSONAGEM GEOMETRICA","BLENDER WORKBENCH PROCEDURAL")
TZ=ZoneInfo("America/Fortaleza")

class GateError(Exception):
    pass

def assert_true(condition,reason):
    if not condition: raise GateError(reason)

def safe_repo_file(rel):
    assert_true(isinstance(rel,str) and rel.strip() and not rel.startswith("/"),
                "Arquivo deve usar caminho relativo do repositório")
    base=ROOT.resolve()
    path=(ROOT/rel).resolve()
    assert_true(path.is_relative_to(base),f"Path fora do repositório: {rel}")
    assert_true(path.exists() and path.is_file(),f"Arquivo não encontrado: {rel}")
    return path

def analyze_video(file):
    try:
        output=subprocess.check_output(["ffprobe","-v","error","-show_entries",
            "stream=codec_type,codec_name,width,height,r_frame_rate:format=duration",
            "-of","json",str(file)],text=True,stderr=subprocess.STDOUT,timeout=50)
        data=json.loads(output)
    except (subprocess.CalledProcessError,FileNotFoundError,ValueError,
            subprocess.TimeoutExpired) as e:
        raise GateError(f"ffprobe não conseguiu validar {file.name}: {e}") from e
    videos=[s for s in data.get("streams",[]) if s.get("codec_type")=="video"]
    audios=[s for s in data.get("streams",[]) if s.get("codec_type")=="audio"]
    assert_true(len(videos)==1 and len(audios)>=1,f"Video/áudio ausente: {file.name}")
    stream=videos[0]
    duration=float(data.get("format",{}).get("duration",0))
    w,h=int(stream.get("width",0)),int(stream.get("height",0))
    assert_true(w>=720 and h>=1280 and abs(w/h-9/16)<.005,
                f"Formato vertical 9:16 inválido: {file.name}")
    assert_true(stream.get("codec_name")=="h264" and audios[0].get("codec_name")=="aac",
                f"Precisa ser H.264/AAC: {file.name}")
    assert_true(61<=duration<=180,
                f"Vídeo exige narrativa de 61–180 segundos: {file.name}: {duration}")
    try:
        p,q=(int(v) for v in stream.get("r_frame_rate","0/1").split("/"))
        fps=p/q
    except (ZeroDivisionError,ValueError):
        fps=0
    assert_true(29<=fps<=60,f"FPS inválido: {file.name}: {fps}")
    # Movimento real mínimo: amostra em 2 fps e mede diferença média de pixels.
    # Partículas microscópicas não devem mascarar uma tela parada por 8–18 s.
    try:
        raw=subprocess.check_output(["ffmpeg","-v","error","-i",str(file),
            "-vf","fps=2,scale=90:160,format=gray","-f","rawvideo","pipe:1"],
            timeout=90)
    except (subprocess.CalledProcessError,subprocess.TimeoutExpired) as e:
        raise GateError(f"FFmpeg não mediu movimento de {file.name}: {e}") from e
    frame_size=90*160
    frames=[raw[i:i+frame_size] for i in range(0,len(raw),frame_size)
            if len(raw[i:i+frame_size])==frame_size]
    assert_true(len(frames)>=120,f"Amostras visuais insuficientes: {file.name}")
    diffs=[sum(abs(a-b) for a,b in zip(before,after))/frame_size
           for before,after in zip(frames,frames[1:])]
    near_static=[value<.30 for value in diffs]
    longest=current=0
    for quiet in near_static:
        current=current+1 if quiet else 0
        longest=max(longest,current)
    static_ratio=sum(near_static)/max(1,len(near_static))
    longest_static_s=longest/2
    assert_true(longest_static_s<=4.0,
                f"Trecho quase estático excede 4 s: {file.name}: {longest_static_s:.1f}s")
    assert_true(static_ratio<=.58,
                f"Movimento insuficiente: {file.name}: {static_ratio:.0%} quase estático")
    return {"file":file.name,"duration_s":round(duration,1),"resolution":f"{w}x{h}",
            "fps":round(fps,2),"near_static_ratio":round(static_ratio,3),
            "longest_near_static_s":round(longest_static_s,1)}

def check_manifest(doc, technical=True, now=None):
    assert_true(isinstance(doc,dict),"Manifesto deve ser objeto JSON")
    assert_true(doc.get("profile")=="@metonalencar","Perfil TikTok diferente do autorizado")
    assert_true(doc.get("timezone")=="America/Fortaleza","Fuso de publicação incorreto")
    assert_true(doc.get("quality_gate_version")==1,"Versão de validação não reconhecida")
    now=now or datetime.now(TZ)
    approval=doc.get("approval")
    assert_true(isinstance(approval,dict),"Evidência de aprovação explícita ausente")
    assert_true(approval.get("user_approved") is True,
                "Usuário ainda não aprovou os quatro vídeos completos")
    assert_true(approval.get("scope")=="four_complete_hybrid_videos",
                "Aprovação não cobre os quatro vídeos híbridos completos")
    raw_approval=approval.get("approved_at")
    assert_true(isinstance(raw_approval,str),"Data da aprovação explícita ausente")
    try:approved_at=datetime.fromisoformat(raw_approval)
    except ValueError:raise GateError(f"Data de aprovação inválida: {raw_approval}")
    assert_true(approved_at.tzinfo is not None,
                "Data de aprovação precisa registrar o fuso horário")
    assert_true(approved_at<=now+timedelta(minutes=5),
                "Data de aprovação está no futuro")
    entries=doc.get("videos")
    assert_true(isinstance(entries,list) and len(entries)==4,"Precisam existir 4 vídeos únicos")
    ids=set();topics=set();dates=set();scheduled=[];reports=[]
    for i,entry in enumerate(entries):
        assert_true(isinstance(entry,dict),f"Entrada {i+1}: item inválido")
        v_id=entry.get("id")
        topic=entry.get("topic")
        assert_true(isinstance(v_id,str) and bool(re.fullmatch(r"[a-z0-9-]{5,80}",v_id)),
                    f"Entrada {i+1}: ID inválido")
        assert_true(isinstance(topic,str) and len(topic.strip())>6,
                    f"Entrada {i+1}: pauta inválida")
        assert_true(v_id not in ids and topic.casefold() not in topics,
                    "Temas ou IDs repetidos na semana")
        ids.add(v_id);topics.add(topic.casefold())
        raw_date=entry.get("publication_date")
        assert_true(isinstance(raw_date,str),"Data agendada ausente")
        try:date=datetime.fromisoformat(raw_date)
        except ValueError:raise GateError(f"Data inválida: {raw_date}")
        assert_true(date.tzinfo is None,"Usar horário local America/Fortaleza sem offset")
        assert_true(date.replace(tzinfo=TZ)>=now+timedelta(hours=2),
                    f"{v_id}: publicação não tem margem futura de 2 horas")
        assert_true(raw_date not in dates,"Duas postagens no mesmo instante")
        dates.add(raw_date)
        scheduled.append(date)
        assert_true(entry.get("generative_ai_label") is True,
                    f"{v_id}: rótulo nativo de IA deve ser enviado ao Metricool")
        assert_true(entry.get("auto_publish") is True,
                    f"{v_id}: o agendamento final deve solicitar autopublicação")
        technique=(entry.get("visual_method") or "").upper()
        assert_true("CGI" in technique and "STATIC" not in technique and
                    not any(x in technique for x in OLD_MARKERS),
                    f"{v_id}: formato visual antigo ou não identificado")
        review=entry.get("visual_review")
        assert_true(isinstance(review,dict),f"{v_id}: revisão audiovisual ausente")
        for key in ("character_fidelity","meaningful_motion","scene_diversity",
                    "spoken_audio_quality","subtitle_legibility","storytelling"):
            assert_true(review.get(key)=="pass",f"{v_id}: revisão {key} não aprovada")
        assert_true(isinstance(review.get("evidence_notes"),str) and
                    len(review["evidence_notes"])>=40,
                    f"{v_id}: explicar evidências da inspeção audiovisual")
        preview=safe_repo_file(review.get("contact_sheet"))
        assert_true(preview.suffix.lower() in (".jpg",".jpeg",".png") and preview.stat().st_size>6000,
                    f"{v_id}: evidência visual ausente/pequena")
        movie=safe_repo_file(entry.get("file"))
        assert_true(movie.suffix.lower()==".mp4" and movie.stat().st_size>100000,
                    f"{v_id}: mídia MP4 ausente/pequena")
        assert_true("/pilotos/" not in str(movie),
                    f"{v_id}: um piloto de demonstração não pode virar postagem sem nova produção")
        if technical:
            reports.append(analyze_video(movie))
    assert_true(scheduled==sorted(scheduled),"Datas devem estar em ordem crescente")
    return reports

def self_test():
    good={"profile":"@metonalencar","timezone":"America/Fortaleza",
          "quality_gate_version":1,"videos":[]}
    try:check_manifest(good,technical=False)
    except GateError:pass
    else:raise AssertionError("Manifesto vazio passou indevidamente")
    try:safe_repo_file("../outside.mp4")
    except GateError:pass
    else:raise AssertionError("Caminho fora do repositório aceito")
    now=datetime(2026,11,28,9,0,tzinfo=TZ)
    expired={"profile":"@metonalencar","timezone":"America/Fortaleza",
             "quality_gate_version":1,"approval":{"user_approved":True,
             "scope":"four_complete_hybrid_videos",
             "approved_at":"2026-11-28T08:00:00-03:00"},"videos":[
             {"id":f"video-{i}","topic":f"Tema original {i}",
              "publication_date":f"2026-11-{20+i:02d}T10:00"}
             for i in range(4)]}
    try:check_manifest(expired,technical=False,now=now)
    except GateError:pass
    else:raise AssertionError("Datas vencidas foram aceitas")
    print("SELF-TEST: gate bloqueia falta de aprovação, datas vencidas e caminhos indevidos")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",default=str(DEFAULT))
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if args.self_test:return self_test()
    path=Path(args.manifest)
    if not path.is_absolute():path=ROOT/path
    if not path.exists():raise GateError(f"Sem lançamento: {path}. Produção não está pronta.")
    doc=json.loads(path.read_text(encoding="utf-8"))
    report=check_manifest(doc)
    print(json.dumps({"technical_gate":"passed","warning":
          "Inspeção de qualidade real e confirmação do Metricool continuam necessárias",
          "videos":report},ensure_ascii=False,indent=2))
if __name__=="__main__":
    try:main()
    except (GateError,ValueError) as exc:
        print("BLOQUEADO: "+str(exc),file=sys.stderr)
        sys.exit(2)
