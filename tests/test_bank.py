import json
from pathlib import Path
bank=json.loads((Path(__file__).resolve().parents[1]/"topics.json").read_text(encoding="utf-8"))
assert len(bank)==24
assert len(set(item["id"] for item in bank))==len(bank)
assert all(len(item["tips"])==4 for item in bank)
assert all(len(tip[1].split())>22 for item in bank for tip in item["tips"])
print("BANCO VALIDADO: 24 roteiros inéditos, 4 dicas por vídeo")
