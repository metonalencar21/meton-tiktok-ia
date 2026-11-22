import bpy, math, sys, os
from mathutils import Vector
out=sys.argv[sys.argv.index('--')+1]
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE' if bpy.app.version<(4,2,0) else 'BLENDER_EEVEE_NEXT'
sc.render.resolution_x=360;sc.render.resolution_y=640;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG'
sc.render.film_transparent=False
sc.world.color=(0.015,0.006,0.03)
sc.frame_start=1;sc.frame_end=144
def mat(name,color,em=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
 if p.inputs.get('Emission Color'):p.inputs['Emission Color'].default_value=(*color,1)
 if p.inputs.get('Emission Strength'):p.inputs['Emission Strength'].default_value=em
 return m
skin=mat('pele',(0.66,.34,.23));hair=mat('cabelo castanho',(.055,.018,.012));hood=mat('moletom preto',(.012,.01,.024));pink=mat('rosa neon',(.85,.015,.28),.5);white=mat('olhos',(.95,.87,.8));iris=mat('iris castanha',(.13,.045,.018));dark=mat('fundo',(.015,.005,.04));screen=mat('tela pix',(.02,.35,.32),.8)
def uv(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material);return o
def cube(name,loc,scale,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);return o
cube('estudio',(0,1.1,1.7),(8,.15,8),dark)
body=uv('moletom',(0,0,1.0),(.74,.36,.87),hood)
uv('capuz', (0,.15,1.65),(.61,.32,.5),pink)
head=uv('rosto',(0,-.19,2.17),(.46,.37,.58),skin)
uv('cabelo topo',(0,-.04,2.61),(.52,.4,.31),hair)
for side in (-1,1):
 uv('cabelo longo',(side*.45,-.025,1.86),(.18,.31,.75),hair)
 uv('olho branco',(side*.18,-.518,2.23),(.145,.06,.105),white)
 uv('iris',(side*.18,-.572,2.23),(.071,.035,.076),iris)
 uv('pupila',(side*.18,-.601,2.23),(.031,.015,.04),hood)
uv('nariz',(0,-.56,2.07),(.065,.075,.09),skin)
mouth=uv('boca',(0,-.551,1.88),(.16,.025,.025),pink)
uv('cordao esquerdo',(-.15,-.36,1.33),(.025,.025,.33),pink)
uv('cordao direito',(.15,-.36,1.33),(.025,.025,.33),pink)
arm=uv('braco em gesto',(.75,-.25,1.12),(.18,.18,.55),hood)
phone=cube('celular 3d pix',(.66,-.54,1.55),(.43,.07,.7),hood)
cube('tela pix',(.66,-.583,1.56),(.34,.02,.55),screen)
for frame in (1,36,72,108,144):
 t=(frame-1)/143
 sc.frame_set(frame)
 head.rotation_euler.z=.07*math.sin(t*math.pi*4)
 head.keyframe_insert(data_path='rotation_euler',frame=frame)
 arm.rotation_euler.y=.16*math.sin(t*math.pi*4)
 arm.keyframe_insert(data_path='rotation_euler',frame=frame)
 phone.location.z=1.55+.12*math.sin(t*math.pi*4)
 phone.keyframe_insert(data_path='location',frame=frame)
 mouth.scale.z=.025+.05*abs(math.sin(t*math.pi*13))
 mouth.keyframe_insert(data_path='scale',frame=frame)
 bpy.context.view_layer.update()
def area(loc,power,color):
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.color=color;l.data.size=4
area((-3,-4,5),600,(1,.25,.55));area((3,-2,4),500,(.3,.4,1))
bpy.ops.object.camera_add(location=(0,-7.8,2.1));cam=bpy.context.object
direction=Vector((0,0,1.65))-cam.location;cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=4.0;sc.camera=cam
os.makedirs(out,exist_ok=True)
for f in range(1,145):
 sc.frame_set(f);sc.render.filepath=os.path.join(out,f'{f:04d}.png');bpy.ops.render.render(write_still=True)
