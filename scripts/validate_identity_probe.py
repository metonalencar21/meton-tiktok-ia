#!/usr/bin/env python3
"""Validação técnica de prova visual; NUNCA aprova postagem."""
import json
import sys
from pathlib import Path

def validate(folder: Path):
    manifest = json.loads((folder / "identidade-rig-probe.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "DEVELOPMENT_IDENTITY_PROBE_NOT_APPROVED"
    assert manifest["probe_revision"] >= 6
    assert manifest["thematic_prop"] == "animated_3d_phone_and_pix_alert_development_only"
    assert len(set(manifest["frames"])) == 3
    assert manifest["resolution"] == "270x480"
    frames = [folder / f"identidade-rig-{i:02d}.png" for i in range(1, 4)]
    for frame in frames:
        data = frame.read_bytes()
        assert data[:8] == b"\\x89PNG\\r\\n\\x1a\\n", frame
        assert int.from_bytes(data[16:20], "big") == 270, frame
        assert int.from_bytes(data[20:24], "big") == 480, frame
        assert len(data) > 10000, frame
    assert len({frame.read_bytes() for frame in frames}) == 3, "Quadros idênticos"
    print("Prova técnica OK; identidade visual e publicação NÃO aprovadas")

if __name__ == "__main__":
    validate(Path(sys.argv[1]))
