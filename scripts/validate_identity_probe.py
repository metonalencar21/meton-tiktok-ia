#!/usr/bin/env python3
"""Validação técnica de prova visual; NUNCA aprova postagem."""
import json
import sys
from pathlib import Path

def validate(folder: Path):
    manifest = json.loads((folder / "identidade-rig-probe.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "DEVELOPMENT_IDENTITY_PROBE_NOT_APPROVED"
    assert manifest["probe_revision"] >= 14
    assert manifest["thematic_prop"] == "animated_3d_phone_and_pix_alert_development_only"
    gesture = manifest["gesture_test"]
    expected_controls = {
        "left_hand": "IK-Hand.L",
        "right_hand": "IK-Hand.R",
        "head": "FK-Head",
    }
    assert gesture["controls_keyframed"] == expected_controls
    assert gesture["phone_anchor"] == "DEF-Hand.R"
    phone_positions = gesture["phone_world_positions"]
    assert len(phone_positions) == 3
    assert len({tuple(position) for position in phone_positions}) == 3, (
        "Celular sem deslocamento comprovado nos quadros revisados"
    )
    view_positions = gesture["phone_view_positions"]
    assert len(view_positions) == 3
    for x, y, depth in view_positions:
        assert 0.12 <= x <= 0.88, "Celular fora do enquadramento horizontal"
        assert 0.14 <= y <= 0.86, "Celular fora do enquadramento vertical"
        assert depth > 0, "Celular atrás da câmera"
    assert len(gesture["phone_anchor_sources"]) == 3
    evidence = manifest["thematic_prop_evidence"]
    assert evidence["assembly_root"] == "METON-PIX-phone-root"
    assert len(evidence["children"]) == 3
    assert len(set(evidence["keyframes"])) == 3
    assert evidence["screen_faces_camera"] is True
    assert len(set(manifest["frames"])) == 3
    assert manifest["resolution"] == "270x480"
    frames = [folder / f"identidade-rig-{i:02d}.png" for i in range(1, 4)]
    for frame in frames:
        data = frame.read_bytes()
        assert data[:8] == bytes.fromhex("89504e470d0a1a0a"), frame
        assert int.from_bytes(data[16:20], "big") == 270, frame
        assert int.from_bytes(data[20:24], "big") == 480, frame
        assert len(data) > 10000, frame
    assert len({frame.read_bytes() for frame in frames}) == 3, "Quadros idênticos"
    print("Prova técnica OK; identidade visual e publicação NÃO aprovadas")

if __name__ == "__main__":
    validate(Path(sys.argv[1]))
