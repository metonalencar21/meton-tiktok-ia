#!/usr/bin/env python3
"""Inventaria um personagem .blend antes de qualquer uso no TikTok IA.

Executar somente dentro do Blender:
  blender -b arquivo.blend --python scripts/inspect_character_rig.py -- \
    --output public/development/rig-inventory.json

Não renderiza, publica, agenda nem marca o personagem como aprovado.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

import bpy


SEMANTIC_PATTERNS = {
    "hands": re.compile(r"(?i)(hand|wrist|palm|finger|thumb)"),
    "arms": re.compile(r"(?i)(arm|elbow|shoulder|clavicle)"),
    "head": re.compile(r"(?i)(head|neck)"),
    "eyes": re.compile(r"(?i)(eye|eyelid|eyering|blink)"),
    "brows": re.compile(r"(?i)(brow|eyebrow)"),
    "mouth": re.compile(r"(?i)(mouth|lip|jaw|tongue|sneer|smile)"),
    "torso": re.compile(r"(?i)(spine|chest|torso|hip|pelvis|root)"),
}


def parse_args() -> argparse.Namespace:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--source", default="unknown")
    parser.add_argument("--license", default="unknown")
    return parser.parse_args(args)


def clean_names(items, limit=80):
    return sorted({str(x) for x in items if x})[:limit]


def semantic_controls(names, limit=120):
    clean = clean_names(names, 10000)
    return {
        category: [name for name in clean if pattern.search(name)][:limit]
        for category, pattern in SEMANTIC_PATTERNS.items()
    }


def animation_binding(obj):
    data = obj.animation_data
    action = data.action.name if data and data.action else None
    strips = []
    if data:
        for track in data.nla_tracks:
            for strip in track.strips:
                strips.append(strip.action.name if strip.action else strip.name)
    drivers = len(data.drivers) if data else 0
    if action or strips or drivers:
        return {
            "object": obj.name,
            "action": action,
            "nla_actions": clean_names(strips, 40),
            "drivers": drivers,
        }
    return None


def main() -> None:
    args = parse_args()
    armatures = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    cameras = [obj for obj in bpy.data.objects if obj.type == "CAMERA"]
    lights = [obj for obj in bpy.data.objects if obj.type == "LIGHT"]

    armature_rows = []
    semantic_rows = []
    deform_bones = 0
    control_bones = 0
    combined_semantics = {name: [] for name in SEMANTIC_PATTERNS}
    for obj in armatures:
        bones = list(obj.data.bones)
        pose_bones = list(obj.pose.bones)
        deform = sum(1 for bone in bones if bone.use_deform)
        deform_bones += deform
        control_bones += max(0, len(pose_bones) - deform)
        names = [bone.name for bone in pose_bones]
        semantics = semantic_controls(names)
        for category, matches in semantics.items():
            combined_semantics[category].extend(matches)
        armature_rows.append({
            "name": obj.name,
            "bones": len(bones),
            "deform_bones": deform,
            "pose_bones": len(pose_bones),
            "sample_bones": clean_names((bone.name for bone in bones), 60),
        })
        semantic_rows.append({
            "armature": obj.name,
            "controls": semantics,
        })

    shape_key_rows = []
    total_shape_keys = 0
    vertices = 0
    for obj in meshes:
        vertices += len(obj.data.vertices)
        blocks = []
        if obj.data.shape_keys:
            blocks = [block.name for block in obj.data.shape_keys.key_blocks]
        total_shape_keys += max(0, len(blocks) - (1 if "Basis" in blocks else 0))
        if blocks:
            shape_key_rows.append({
                "object": obj.name,
                "shape_keys": clean_names(blocks, 120),
                "semantic_shape_keys": semantic_controls(blocks, 120),
            })

    material_names = clean_names((mat.name for mat in bpy.data.materials), 120)
    action_names = clean_names((action.name for action in bpy.data.actions), 80)
    object_names = clean_names((obj.name for obj in bpy.data.objects), 160)
    bindings = [row for obj in bpy.data.objects if (row := animation_binding(obj))]
    combined_semantics = {
        category: clean_names(matches, 200)
        for category, matches in combined_semantics.items()
    }

    checks = {
        "has_armature": len(armatures) >= 1,
        "production_bone_count": deform_bones >= 40,
        "has_face_or_expression_system": total_shape_keys >= 8 or control_bones >= 20,
        "has_separate_mesh_parts": len(meshes) >= 3,
        "nontrivial_mesh": vertices >= 10000,
        "has_materials": len(material_names) >= 3,
    }
    performance_controls = {
        "hands": bool(combined_semantics["hands"]),
        "head": bool(combined_semantics["head"]),
        "gaze": bool(combined_semantics["eyes"]),
        "facial_expression": bool(
            combined_semantics["brows"] and combined_semantics["mouth"]
        ),
    }
    report = {
        "schema_version": 2,
        "purpose": "development_inventory_only",
        "source": args.source,
        "license": args.license,
        "identity_status": "NOT_APPROVED_BASE_RIG",
        "warning": (
            "Capacidade de rig não comprova fidelidade à personagem oficial. "
            "Cabelo, rosto, moletom preto/rosa, atuação e cenas ainda exigem adaptação e revisão visual."
        ),
        "counts": {
            "armatures": len(armatures),
            "meshes": len(meshes),
            "vertices": vertices,
            "deform_bones": deform_bones,
            "control_bones_estimate": control_bones,
            "shape_keys_without_basis": total_shape_keys,
            "materials": len(material_names),
            "actions": len(action_names),
            "cameras": len(cameras),
            "lights": len(lights),
            "animation_bindings": len(bindings),
        },
        "checks": checks,
        "rig_capability_candidate": all(checks.values()),
        "performance_controls": performance_controls,
        "thematic_animation_candidate": all(performance_controls.values()),
        "semantic_controls": semantic_rows,
        "semantic_controls_combined": combined_semantics,
        "animation_bindings": bindings,
        "armatures": armature_rows,
        "shape_keys": shape_key_rows,
        "materials": material_names,
        "actions": action_names,
        "objects": object_names,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "rig_capability_candidate": report["rig_capability_candidate"],
        "thematic_animation_candidate": report["thematic_animation_candidate"],
        "performance_controls": report["performance_controls"],
        "counts": report["counts"],
        "failed_checks": [name for name, ok in checks.items() if not ok],
        "output": str(output),
    }, ensure_ascii=False, indent=2))

    if not report["rig_capability_candidate"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
