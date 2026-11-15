#!/usr/bin/env python3
"""Cria uma prova visual vertical da base articulada com a paleta oficial.

Executar dentro do Blender já com o arquivo Rain carregado. O resultado é
somente desenvolvimento: não é episódio, não é candidato de release e não
autoriza publicação.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector


def parse_args() -> argparse.Namespace:
    values = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args(values)


def set_principled(material_name: str, color, metallic=0.0, roughness=0.42):
    material = bpy.data.materials.get(material_name)
    if not material:
        return False
    material.use_nodes = True
    nodes = material.node_tree.nodes
    shader = next((node for node in nodes if node.type == "BSDF_PRINCIPLED"), None)
    if shader is None:
        return False
    base = shader.inputs.get("Base Color")
    if base:
        for link in list(base.links):
            material.node_tree.links.remove(link)
        base.default_value = color
    if shader.inputs.get("Metallic"):
        shader.inputs["Metallic"].default_value = metallic
    if shader.inputs.get("Roughness"):
        shader.inputs["Roughness"].default_value = roughness
    return True


def make_material(name: str, color, emission_strength=0.0):
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.use_nodes = True
    shader = next(node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Roughness"].default_value = 0.32
    emission = shader.inputs.get("Emission Color") or shader.inputs.get("Emission")
    if emission:
        emission.default_value = color
    strength = shader.inputs.get("Emission Strength")
    if strength:
        strength.default_value = emission_strength
    return material


def assign(obj, material):
    obj.data.materials.clear()
    obj.data.materials.append(material)


def look_at(obj, target: Vector):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def character_bounds(objects):
    points = []
    for obj in objects:
        for corner in obj.bound_box:
            points.append(obj.matrix_world @ Vector(corner))
    if not points:
        raise RuntimeError("Nenhuma malha renderizável GEO-rain encontrada")
    minimum = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    maximum = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return minimum, maximum


def cube(name, location, scale, material):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    assign(obj, material)
    return obj


def main():
    args = parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    # O identificador do Eevee mudou entre versões empacotadas do Blender.
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = engine
            break
        except TypeError:
            continue
    else:
        raise RuntimeError("Eevee não está disponível; Workbench não é aceito para esta prova")
    scene.render.resolution_x = 270
    scene.render.resolution_y = 480
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.resolution_percentage = 100
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    scene.world.color = (0.003, 0.001, 0.012)

    # Mantém apenas a personagem e o rig necessário; remove o cenário benchmark.
    character = [
        obj for obj in bpy.data.objects
        if obj.type == "MESH" and obj.name.startswith("GEO-rain") and not obj.hide_render
    ]
    keep_prefixes = ("GEO-rain", "RIG-rain", "CH-rain")
    for obj in bpy.data.objects:
        if obj.name.startswith(keep_prefixes):
            continue
        if obj.type in {"MESH", "CURVE", "FONT", "LIGHT", "CAMERA"}:
            obj.hide_render = True

    palette_changes = {
        "MAT-rain.hair": set_principled("MAT-rain.hair", (0.045, 0.010, 0.006, 1), roughness=0.3),
        "MAT-rain.hairband": set_principled("MAT-rain.hairband", (0.92, 0.012, 0.30, 1), metallic=0.1),
        "MAT-rain.top": set_principled("MAT-rain.top", (0.008, 0.010, 0.018, 1), roughness=0.48),
        "MAT-rain.scarf": set_principled("MAT-rain.scarf", (0.85, 0.008, 0.24, 1), roughness=0.36),
        "MAT-rain.eyes": set_principled("MAT-rain.eyes", (0.16, 0.035, 0.012, 1), roughness=0.22),
        "MAT-rain.eyebrows": set_principled("MAT-rain.eyebrows", (0.03, 0.006, 0.004, 1), roughness=0.4),
    }

    scene.frame_set(scene.frame_start)
    bpy.context.view_layer.update()
    minimum, maximum = character_bounds(character)
    center = (minimum + maximum) * 0.5
    size = maximum - minimum
    height = max(size.z, 1.0)
    width = max(size.x, 0.5)

    dark = make_material("METON-neon-dark", (0.006, 0.002, 0.025, 1))
    pink = make_material("METON-neon-pink", (0.95, 0.005, 0.32, 1), 7.0)
    cyan = make_material("METON-neon-cyan", (0.005, 0.38, 0.62, 1), 5.0)

    # Estúdio simples, construído em 3D; não é slide ou painel.
    cube("METON-backdrop", (center.x, maximum.y + height * 0.55, center.z), (width * 2.4, 0.08, height * 0.8), dark)
    cube("METON-neon-left", (center.x - width * 1.25, maximum.y + height * 0.38, center.z + height * 0.05), (0.035, 0.035, height * 0.62), pink)
    cube("METON-neon-right", (center.x + width * 1.25, maximum.y + height * 0.38, center.z - height * 0.02), (0.035, 0.035, height * 0.62), cyan)
    cube("METON-floor", (center.x, center.y, minimum.z - 0.035), (width * 2.5, height * 1.5, 0.03), dark)

    for name, color, energy, offset in (
        ("METON-key-pink", (1.0, 0.02, 0.26), 900, (-width * 1.7, -height * 0.5, height * 0.55)),
        ("METON-fill-blue", (0.02, 0.22, 1.0), 750, (width * 1.6, -height * 0.15, height * 0.3)),
        ("METON-rim-purple", (0.55, 0.01, 1.0), 1100, (0, height * 0.65, height * 0.75)),
    ):
        bpy.ops.object.light_add(type="AREA", location=center + Vector(offset))
        light = bpy.context.object
        light.name = name
        light.data.color = color
        light.data.energy = energy
        light.data.shape = "DISK"
        light.data.size = height * 0.9
        light.data.use_shadow = False
        look_at(light, center)

    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "METON-camera-vertical"
    distance = max(height * 1.55, width * 3.0)
    camera.location = center + Vector((0, -distance, height * 0.07))
    camera.data.lens = 58
    camera.data.dof.use_dof = False
    camera.data.dof.focus_object = next((o for o in character if o.name == "GEO-rain_head"), character[0])
    camera.data.dof.aperture_fstop = 4.0
    look_at(camera, center + Vector((0, 0, height * 0.06)))
    scene.camera = camera

    span = max(1, scene.frame_end - scene.frame_start)
    frames = [
        scene.frame_start + int(span * 0.16),
        scene.frame_start + int(span * 0.50),
        scene.frame_start + int(span * 0.84),
    ]
    rendered = []
    for index, frame in enumerate(frames, 1):
        scene.frame_set(frame)
        scene.render.filepath = str(out / f"identidade-rig-{index:02d}.png")
        bpy.ops.render.render(write_still=True)
        rendered.append(scene.render.filepath)

    report = {
        "status": "DEVELOPMENT_IDENTITY_PROBE_NOT_APPROVED",
        "frames": frames,
        "rendered": rendered,
        "resolution": "270x480",
        "engine": scene.render.engine,
        "palette_changes": palette_changes,
        "character_bounds": {
            "minimum": list(minimum),
            "maximum": list(maximum),
            "height": height,
            "width": width,
        },
        "warning": (
            "A prova testa paleta, iluminação e articulação. Não comprova cabelo longo, "
            "moletom fiel, atuação temática, sincronização labial ou aprovação final."
        ),
    }
    (out / "identidade-rig-probe.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
