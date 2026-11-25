#!/usr/bin/env python3
"""Promove quatro híbridos aprovados para candidatos de publicação.

Não agenda, não publica e não altera o catálogo. A promoção só ocorre quando o
catálogo registra aprovação explícita do usuário e revisão audiovisual completa.
"""
import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"public/pilotos/catalogo_hibrido_2026-11-22.json"
OUT=ROOT/"public/release-candidates"
MANIFEST=OUT/"semana-atual.json"
TZ=ZoneInfo("America/Fortaleza")
PASS_KEYS=("character_fidelity","meaningful_motion","scene_diversity",
           "spoken_audio_quality","subtitle_legibility","storytelling")

class ApprovalError(Exception):
    pass

def require(condition,message):
    if not condition:raise ApprovalError(message)

def validate_approval(catalog):
    require(catalog.get("profile")=="@metonalencar","Perfil divergente")
    require(catalog.get("timezone")=="America/Fortaleza","Fuso divergente")
    require(catalog.get("approved") is True,"Sem aprovação explícita do formato")
    approval=catalog.get("approval")
    require(isinstance(approval,dict),"Evidência de aprovação ausente")
    require(approval.get("user_approved") is True,"Usuário não aprovou os quatro MP4s")
    require(approval.get("scope")=="four_complete_hybrid_videos",
            "Escopo de aprovação não cobre os quatro vídeos completos")
    require(isinstance(approval.get("approved_at"),str),"Data de aprovação ausente")
    try:datetime.fromisoformat(approval["approved_at"])
    except ValueError as exc:raise ApprovalError("Data de aprovação inválida") from exc
    videos=catalog.get("videos")
    require(isinstance(videos,list) and len(videos)==4,"Catálogo precisa de quatro vídeos")
    for item in videos:
        require(item.get("approved") is True,f"{item.get('id')}: aprovação individual ausente")
        review=item.get("visual_review")
        require(isinstance(review,dict),f"{item.get('id')}: revisão audiovisual ausente")
        for key in PASS_KEYS:
            require(review.get(key)=="pass",f"{item.get('id')}: {key} não passou")
        require(len(review.get("evidence_notes","").strip())>=40,
                f"{item.get('id')}: evidência audiovisual insuficiente")
        source=(ROOT/item.get("file","")).resolve()
        require(source.is_relative_to(ROOT) and source.is_file(),
                f"{item.get('id')}: MP4 não encontrado")
        require(source.suffix.lower()==".mp4",f"{item.get('id')}: mídia não é MP4")
    return videos

def validate_dates(values,now=None):
    require(len(values)==4,"Forneça exatamente quatro datas futuras")
    now=now or datetime.now(TZ)
    parsed=[]
    for raw in values:
        try:value=datetime.fromisoformat(raw)
        except ValueError as exc:raise ApprovalError(f"Data inválida: {raw}") from exc
        require(value.tzinfo is None,"Datas devem usar horário local sem offset")
        local=value.replace(tzinfo=TZ)
        require(local>=now+timedelta(hours=2),f"Data não é futura com margem segura: {raw}")
        parsed.append(value)
    require(len({x.isoformat() for x in parsed})==4,"Datas de publicação repetidas")
    require(parsed==sorted(parsed),"Datas devem estar em ordem crescente")
    return parsed

def contact_sheet(movie,target):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(movie),
        "-vf","fps=1/7.5,scale=180:320:flags=lanczos,tile=4x3:padding=4:margin=4",
        "-frames:v","1","-q:v","3",str(target)],check=True,timeout=120)
    require(target.is_file() and target.stat().st_size>6000,
            f"Folha de contato inválida: {target.name}")

def promote(catalog,dates,dry_run=False):
    videos=validate_approval(catalog)
    dates=validate_dates(dates)
    if dry_run:return {"status":"ready_to_promote","videos":len(videos)}
    OUT.mkdir(parents=True,exist_ok=True)
    entries=[]
    for item,date in zip(videos,dates):
        source=(ROOT/item["file"]).resolve()
        movie=OUT/f"{item['id']}.mp4"
        sheet=OUT/f"{item['id']}-contact.jpg"
        shutil.copy2(source,movie)
        contact_sheet(movie,sheet)
        review=item["visual_review"]
        entries.append({
          "id":item["id"],"topic":item["title"],
          "publication_date":date.isoformat(timespec="minutes"),
          "generative_ai_label":True,"auto_publish":True,
          "visual_method":"HYBRID CGI 2.5D + ANIMATED TOPIC-SPECIFIC UI",
          "file":movie.relative_to(ROOT).as_posix(),
          "visual_review":{**{key:"pass" for key in PASS_KEYS},
            "evidence_notes":review["evidence_notes"],
            "contact_sheet":sheet.relative_to(ROOT).as_posix()}
        })
    document={"profile":"@metonalencar","timezone":"America/Fortaleza",
              "quality_gate_version":1,"source_catalog":CATALOG.relative_to(ROOT).as_posix(),
              "approval":catalog["approval"],"videos":entries}
    MANIFEST.write_text(json.dumps(document,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"status":"promoted_not_scheduled","manifest":MANIFEST.relative_to(ROOT).as_posix(),
            "videos":len(entries)}

def self_test():
    fake={"profile":"@metonalencar","timezone":"America/Fortaleza","approved":False,
          "videos":[]}
    try:validate_approval(fake)
    except ApprovalError:pass
    else:raise AssertionError("Catálogo não aprovado foi aceito")
    future=(datetime.now(TZ)+timedelta(days=3)).replace(tzinfo=None,second=0,microsecond=0)
    try:validate_dates([future.isoformat()]*4)
    except ApprovalError:pass
    else:raise AssertionError("Datas repetidas foram aceitas")
    print("SELF-TEST: promoção bloqueia falta de aprovação e datas repetidas")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--catalog",default=str(CATALOG))
    parser.add_argument("--date",action="append",default=[])
    parser.add_argument("--dry-run",action="store_true")
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:return self_test()
    catalog=json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    print(json.dumps(promote(catalog,args.date,args.dry_run),ensure_ascii=False,indent=2))

if __name__=="__main__":
    try:main()
    except (ApprovalError,subprocess.CalledProcessError,FileNotFoundError) as exc:
        print("BLOQUEADO: "+str(exc),file=sys.stderr)
        sys.exit(2)
