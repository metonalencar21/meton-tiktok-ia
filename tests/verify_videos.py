from fractions import Fraction
import json
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/"public/manifest.json").read_text(encoding="utf-8"))
assert len(manifest["videos"])==4
for obj in manifest["videos"]:
    p=root/"public"/obj["file"]
    assert p.is_file(),p
    data=json.loads(subprocess.check_output(["ffprobe","-v","error",
        "-show_entries","stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate:format=duration",
        "-of","json",str(p)]))
    vs=[s for s in data["streams"] if s["codec_type"]=="video"]
    au=[s for s in data["streams"] if s["codec_type"]=="audio"]
    assert len(vs)==1 and len(au)==1
    assert vs[0]["codec_name"]=="h264"
    assert Fraction(vs[0]["avg_frame_rate"]) == 30, "TikTok exige 30 FPS neste projeto"
    assert vs[0]["width"]==720 and vs[0]["height"]==1280
    assert float(data["format"]["duration"])>=61
    assert obj["ai_generated"] and obj["quality_review_required"]
    print("VALIDADO",p.name)
