#!/usr/bin/env python3
"""Cria uma prova visual vertical da base articulada com a paleta oficial.

Executar dentro do Blender já com o arquivo Rain carregado. O resultado é
somente desenvolvimento: não é episódio, não é candidato de release e não
autoriza publicação.
"""
from __future__ import annotations

import argparse
import json
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
    shaders = [
        node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED"
    ]
    if not shaders:
        return False
    for shader in shaders:
        base = shader.inputs.get("Base Color")
        if base:
            for link in list(base.links):
                material.node_tree.links.remove(link)
            base.default_value = color
        if shader.inputs.get("Metallic"):
            shader.inputs["Metallic"].default_value = metallic
        if shader.inputs.get("Roughness"):
            shader.inputs["Roughness"].default_value = roughness
        # A primeira prova estourou os olhos. Materiais da personagem não podem
        # emitir luz; só as barras do cenário usam emissão deliberada.
        emission = shader.inputs.get("Emission Color") or shader.inputs.get("Emission")
        if emission:
            for link in list(emission.links):
                material.node_tree.links.remove(link)
            emission.default_value = color
        strength = shader.inputs.get("Emission Strength")
        if strength:
            strength.default_value = 0.0
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


def force_simple_material(name: str, color, roughness=0.35):
    """Substitui materiais de olhos do benchmark por um shader previsível.

    Alguns materiais originais terminam em grupos/emissão e ignoram a edição
    do Principled encontrado. A prova precisa mostrar a íris, não preservar o
    look do benchmark.
    """
    material = bpy.data.materials.get(name)
    if not material:
        return False
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Roughness"].default_value = roughness
    strength = shader.inputs.get("Emission Strength")
    if strength:
        strength.default_value = 0.0
    material.node_tree.links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return True


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
    # O benchmark traz um compositor cinematográfico próprio. Ele foi a causa
    # provável do halo branco nos olhos e não pertence ao estúdio do canal.
    scene.use_nodes = False
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    scene.world.color = (0.003, 0.001, 0.012)

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

    palette_targets = {
        "MAT-rain.hair": ((0.045, 0.010, 0.006, 1), 0.0, 0.30),
        "MAT-rain.hairband": ((0.92, 0.012, 0.30, 1), 0.1, 0.36),
        "MAT-rain.top": ((0.008, 0.010, 0.018, 1), 0.0, 0.48),
        "MAT-rain.scarf": ((0.85, 0.008, 0.24, 1), 0.0, 0.36),
        "MAT-rain.eyes": ((0.12, 0.025, 0.008, 1), 0.0, 0.28),
        "MAT-rain.eyedot": ((0.018, 0.004, 0.002, 1), 0.0, 0.26),
        "MAT-rain.eyes.viewport_blue": ((0.12, 0.025, 0.008, 1), 0.0, 0.28),
        "MAT-rain.eyes.viewport_black": ((0.006, 0.002, 0.001, 1), 0.0, 0.30),
        "MAT-rain.eyes.viewport_white": ((0.72, 0.62, 0.52, 1), 0.0, 0.52),
        "MAT-rain.cornea": ((0.28, 0.16, 0.12, 1), 0.0, 0.08),
        "MAT-rain.eyebrows": ((0.03, 0.006, 0.004, 1), 0.0, 0.40),
    }
    palette_changes = {
        name: set_principled(name, color, metallic=metallic, roughness=roughness)
        for name, (color, metallic, roughness) in palette_targets.items()
    }
    # Os olhos continuaram brancos na revisão 3 apesar de emissão zerada. A
    # revisão 4 troca apenas a cadeia final desses materiais por BSDF simples.
    eye_shader_overrides = {
        "MAT-rain.eyes": force_simple_material(
            "MAT-rain.eyes", (0.11, 0.018, 0.006, 1), 0.30
        ),
        "MAT-rain.eyedot": force_simple_material(
            "MAT-rain.eyedot", (0.004, 0.001, 0.001, 1), 0.28
        ),
        "MAT-rain.eyes.viewport_blue": force_simple_material(
            "MAT-rain.eyes.viewport_blue", (0.11, 0.018, 0.006, 1), 0.30
        ),
        "MAT-rain.eyes.viewport_black": force_simple_material(
            "MAT-rain.eyes.viewport_black", (0.004, 0.001, 0.001, 1), 0.28
        ),
        "MAT-rain.eyes.viewport_white": force_simple_material(
            "MAT-rain.eyes.viewport_white", (0.42, 0.30, 0.23, 1), 0.55
        ),
    }
    # O inventário da revisão 5 mostrou que GEO-rain_eye_cornea é uma casca
    # separada (Glossy + Refraction) sobre a íris. No Eevee headless ela fica
    # branca e encobre os materiais castanhos. A prova desativa somente essa
    # casca; um shader de córnea compatível será necessário no modelo final.
    hidden_cornea_objects = []
    for obj in bpy.data.objects:
        if obj.name.startswith("GEO-rain_eye_cornea"):
            obj.hide_render = True
            hidden_cornea_objects.append(obj.name)

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

    cube("METON-backdrop", (center.x, maximum.y + height * 0.55, center.z), (width * 2.4, 0.08, height * 0.8), dark)
    cube("METON-neon-left", (center.x - width * 1.25, maximum.y + height * 0.38, center.z + height * 0.05), (0.035, 0.035, height * 0.62), pink)
    cube("METON-neon-right", (center.x + width * 1.25, maximum.y + height * 0.38, center.z - height * 0.02), (0.035, 0.035, height * 0.62), cyan)
    cube("METON-floor", (center.x, center.y, minimum.z - 0.035), (width * 2.5, height * 1.5, 0.03), dark)

    # Prop temático real em 3D, não um cartão sobreposto na edição.
    # Revisão 9: o conjunto é rigidamente agrupado e ancorado na faixa inferior do
    # enquadramento vertical. A revisão 6 o colocou fora do campo da câmera.
    phone_shell = make_material("METON-phone-shell", (0.012, 0.014, 0.027, 1))
    phone_screen = make_material("METON-phone-screen", (0.018, 0.10, 0.24, 1), 0.6)
    phone_alert = make_material("METON-phone-alert", (0.95, 0.008, 0.10, 1), 2.0)
    prop_x = center.x + width * 0.12
    prop_y = minimum.y - height * 0.06
    prop_z = minimum.z + height * 0.49

    phone_root = bpy.data.objects.new("METON-PIX-phone-root", None)
    bpy.context.collection.objects.link(phone_root)
    phone_root.location = (prop_x, prop_y, prop_z)

    shell = cube("METON-PIX-phone-3d", (0, 0, 0),
                 (width * 0.08, height * 0.014, height * 0.105), phone_shell)
    screen = cube("METON-PIX-screen-3d", (0, -height * 0.016, 0),
                  (width * 0.067, height * 0.004, height * 0.087), phone_screen)
    alert = cube("METON-PIX-alert-3d", (0, -height * 0.022, height * 0.025),
                 (width * 0.05, height * 0.005, height * 0.018), phone_alert)
    phone_parts = [shell, screen, alert]
    for part in phone_parts:
        part.parent = phone_root
        part.hide_render = False

    # Três batidas dentro do close: entrada curta, alerta máximo e recuo.
    # Só o root se move; tela e alerta não podem descolar da carcaça.
    phone_keyframes = (
        (scene.frame_start, width * 0.04, -height * 0.025, 0.35),
        (scene.frame_start + int((scene.frame_end-scene.frame_start)*0.5), 0.0, 0.0, 1.0),
        (scene.frame_end, -width * 0.025, height * 0.018, 0.55),
    )
    for frame_number, dx, dz, alert_size in phone_keyframes:
        phone_root.location = (prop_x + dx, prop_y, prop_z + dz)
        phone_root.keyframe_insert(data_path="location", frame=frame_number)
        alert.scale.x = width * 0.05 * alert_size
        alert.keyframe_insert(data_path="scale", frame=frame_number)

    for name, color, energy, offset in (
        ("METON-key-pink", (1.0, 0.02, 0.26), 120, (-width * 1.7, -height * 0.5, height * 0.55)),
        ("METON-fill-blue", (0.02, 0.22, 1.0), 85, (width * 1.6, -height * 0.15, height * 0.3)),
        ("METON-rim-purple", (0.55, 0.01, 1.0), 160, (0, height * 0.65, height * 0.75)),
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

    # A prova anterior enquadrou o corpo inteiro pequeno demais. Esta versão
    # testa deliberadamente plano médio/close, sem fingir que corrige a identidade.
    subject_target = Vector((center.x, center.y, minimum.z + height * 0.72))
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "METON-camera-medium-close"
    distance = max(height * 0.52, width * 1.1)
    camera.location = subject_target + Vector((0, -distance, 0))
    camera.data.lens = 50
    camera.data.dof.use_dof = False
    look_at(camera, subject_target)
    scene.camera = camera

    # Movimento de câmera real para evitar a sensação de imagem parada:
    # aproximação curta e micro-deslocamento lateral acompanhando a entrada do prop.
    camera.location = subject_target + Vector((0, -distance * 1.06, height * 0.015))
    camera.keyframe_insert(data_path="location", frame=scene.frame_start)
    camera.location = subject_target + Vector((width * 0.035, -distance, height * 0.02))
    camera.keyframe_insert(data_path="location", frame=scene.frame_start + int((scene.frame_end-scene.frame_start)*0.5))
    camera.location = subject_target + Vector((-width * 0.02, -distance * 0.98, height * 0.01))
    camera.keyframe_insert(data_path="location", frame=scene.frame_end)

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
        "probe_revision": 10,
        "frames": frames,
        "thematic_prop": "animated_3d_phone_and_pix_alert_development_only",
        "thematic_prop_evidence": {
            "assembly_root": phone_root.name,
            "children": [part.name for part in phone_parts],
            "base_location": list((prop_x, prop_y, prop_z)),
            "keyframes": [item[0] for item in phone_keyframes],
            "screen_faces_camera": True,
            "camera_motion": "push_in_and_lateral_micro_shift",
        },
        "rendered": rendered,
        "resolution": "270x480",
        "engine": scene.render.engine,
        "framing": "medium_close_development",
        "eye_emission_disabled": True,
        "benchmark_compositor_disabled": True,
        "eye_shader_overrides": eye_shader_overrides,
        "hidden_cornea_objects": hidden_cornea_objects,
        "palette_changes": palette_changes,
        "character_bounds": {
            "minimum": list(minimum),
            "maximum": list(maximum),
            "height": height,
            "width": width,
        },
        "camera": {
            "target": list(subject_target),
            "distance": distance,
            "lens_mm": camera.data.lens,
        },
        "warning": (
            "A prova revisao 10 adiciona movimento real de câmera e mantém olhos castanhos e ancora o celular PIX na faixa inferior do close. Não comprova cabelo longo, "
            "moletom fiel, atuação temática, sincronização labial ou aprovação final."
        ),
    }
    (out / "identidade-rig-probe.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
