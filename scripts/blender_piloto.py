#!/usr/bin/env python3
"""Protótipo real em Blender 3D: apresentadora feminina, rig simples, celular e câmera animados.
Exclusivamente piloto NÃO APROVADO, sem postagem. CC0 para formas criadas por este script.
Execução: blender -b -t 2 -P scripts/blender_piloto.py -- <pasta> <segundos>
"""
import bpy, math, os, sys, random
from mathutils import Vector

argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT=argv[0] if argv else "/tmp/tiktok3d"
SECS=float(argv[1]) if len(argv)>1 else 11.
FPS=12
N=int(SECS*FPS)
os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
sc.render.engine="BLENDER_WORKBENCH"
sc.display.shading.light="STUDIO"
sc.display.shading.studio_light="paint.sl"
sc.display.shading.color_type="MATERIAL"
sc.display.shading.show_shadows=True
sc.display.shading.show_cavity=True
sc.display.shading.cavity_type="BOTH"
sc.display.shading.curvature_ridge_factor=1.2
sc.display.shading.curvature_valley_factor=0.7
sc.render.resolution_x=360
sc.render.resolution_y=640
sc.render.resolution_percentage=100
sc.render.image_settings.file_format="PNG"
sc.render.film_transparent=False
sc.render.fps=FPS
sc.frame_start=1
sc.frame_end=N
sc.render.filepath=OUT+"/frame_"
sc.world.color=(.028,.028,.075)
bpy.context.view_layer.update()

def mat(name,rgba):
 m=bpy.data.materials.new(name)
 m.diffuse_color=rgba
 return m
skin=mat("pele quente",(.91,.61,.45,1))
pink=mat("rosa neon",(.98,.03,.4,1))
pinklight=mat("reflexos rosa",(.99,.34,.63,1))
black=mat("moletom grafite",(.035,.045,.09,1))
navy=mat("cafe noturno",(.035,.045,.12,1))
purple=mat("cafe roxo",(.16,.085,.34,1))
cyan=mat("turquesa",(.02,.8,.91,1))
white=mat("branco",(.91,.94,1,1))
brown=mat("cabelo castanho escuro",(.155,.065,.05,1))
hairlight=mat("reflexo castanho",(.31,.125,.09,1))
iris=mat("iris",(.19,.07,.04,1))
dark=mat("preto olhos",(.008,.014,.023,1))
red=mat("aviso vermelho",(.91,.07,.13,1))
gray=mat("metal",(.3,.37,.51,1))
lime=mat("alerta amarelo",(.99,.73,.09,1))
pinkbg=mat("vidro rosa",(.37,.09,.24,1))

def smooth(obj):
 if obj.type=="MESH":
  for p in obj.data.polygons: p.use_smooth=True
 return obj
def uv(name,location,scale,material,parent=None,segments=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=16,location=location)
 ob=bpy.context.object;ob.name=name
 ob.scale=scale;ob.data.materials.append(material)
 if parent: ob.parent=parent;ob.matrix_parent_inverse=parent.matrix_world.inverted()
 return smooth(ob)
def cube(name,loc,scale,material,bev=0,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
 ob=bpy.context.object;ob.name=name;ob.dimensions=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 ob.data.materials.append(material)
 if bev:
  m=ob.modifiers.new("rounded corners","BEVEL");m.width=bev;m.segments=3
  ob.modifiers.new("weighted normals","WEIGHTED_NORMAL")
 if parent: ob.parent=parent;ob.matrix_parent_inverse=parent.matrix_world.inverted()
 return ob
def curve(name,coords,rad,material,parent=None):
 cu=bpy.data.curves.new(name,"CURVE");cu.dimensions="3D";cu.bevel_depth=rad;cu.bevel_resolution=2
 spline=cu.splines.new("BEZIER");spline.bezier_points.add(len(coords)-1)
 for bp,co in zip(spline.bezier_points,coords):
  bp.co=co;bp.handle_left_type="AUTO";bp.handle_right_type="AUTO"
 ob=bpy.data.objects.new(name,cu);sc.collection.objects.link(ob);ob.data.materials.append(material)
 if parent: ob.parent=parent;ob.matrix_parent_inverse=parent.matrix_world.inverted()
 return ob
def text3d(name,value,loc,size,material,parent=None):
 cu=bpy.data.curves.new(name,"FONT");cu.body=value;cu.size=size;cu.extrude=.004;cu.bevel_depth=.001
 ob=bpy.data.objects.new(name,cu);sc.collection.objects.link(ob);ob.location=loc;ob.rotation_euler[0]=math.pi/2
 cu.materials.append(material)
 if parent: ob.parent=parent;ob.matrix_parent_inverse=parent.matrix_world.inverted()
 return ob
def empty(name,loc,parent=None):
 ob=bpy.data.objects.new(name,None);sc.collection.objects.link(ob)
 ob.location=loc
 if parent: ob.parent=parent
 return ob
def key(ob,prop,at,values):
 for fr,value in zip(at,values):
  if prop=="location": ob.location=value
  elif prop=="rotation_euler": ob.rotation_euler=value
  elif prop=="scale": ob.scale=value
  elif prop=="lens": ob.data.ortho_scale=value
  if prop=="lens": ob.data.keyframe_insert(data_path="ortho_scale",frame=fr)
  else: ob.keyframe_insert(data_path=prop,frame=fr)
def point_cam(cam,pt):
 direction=Vector(pt)-cam.location
 cam.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()

# Cafe set: physical geometry with a long counter, glowing colors and props
cube("piso", (0,0,-.10),(12,12,.2),navy,.02)
cube("parede", (0,2.8,2.6),(12,.16,6),purple,.03)
cube("balcao",(-2,.4,.81),(2.4,1.2,.1),black,.06)
cube("borda rosa balcao",(-2,-.17,.87),(2.4,.07,.035),pink,.008)
for i in range(10):
 xx=-4.8+i*1.07
 cube("faixa neon", (xx,2.68,1.6+ (i%3)*.72),(.08,.1,.45),pink if i%2 else cyan,.02)
for i in range(12):
 xx=-4+i*.8
 zz=2.0+(i%4)*.4
 uv("luz cafe", (xx,2.35,zz),(.05,.05,.05),pinklight if i%2 else cyan)
# billboard
cube("placa", (1.35,1.65,2.25),(1.85,.11,.95),black,.13)
text3d("WIFI cafe","WI-FI  GRÁTIS",(0.5,1.56,2.17),.22,cyan)
# Table & cup
cube("mesa",(.3,-.8,.82),(2.0,1.05,.13),purple,.08)
cube("perna mesa",(.3,-.8,.36),(.14,.14,.7),gray,.02)
uv("xicara",(-.35,-.64,.97),(.18,.17,.14),white)

# Character root, mostly local-space transforms; face & hair are 3D geometry.
root=empty("RIG: corpo",(-.46,-.14,0))
body=uv("moletom preto",(-.46,-.14,1.13),(.55,.32,.66),black,parent=root)
uv("capuz ombro esq",(-.83,-.12,1.43),(.21,.28,.26),black,parent=root)
uv("capuz ombro dir",(-.08,-.12,1.43),(.21,.28,.26),black,parent=root)
curve("borda rosa casaco",[(-.73,-.47,1.66),(-.61,-.48,1.46),(-.48,-.49,1.24),(-.35,-.46,1.47),(-.23,-.42,1.64)],.028,pink,parent=root)
cube("logo rosa na roupa",(-.47,-.46,1.05),(.19,.03,.16),pink,.03,parent=root)
uv("gola",(-.46,-.14,1.61),(.23,.23,.16),black,parent=root)
uv("pescoco",(-.46,-.14,1.78),(.16,.16,.22),skin,parent=root)
# head pivot: head parts local, because moving pivot must move together
head=empty("RIG: cabeca",(-.46,-.13,1.93),root)
uv("cabelo volume de tras",(-.46,-.055,2.19),(.59,.39,.62),brown,parent=head)
uv("rosto",(-.46,-.315,2.27),(.46,.34,.53),skin,parent=head)
uv("queixo",(-.46,-.41,1.98),(.29,.23,.20),skin,parent=head)
# Hair parted and cascading past shoulders, curved actual 3D strands
for side in [-1,1]:
 xx=-.46+side*.38
 for j in range(5):
  spread=(j-2)*.042
  curve("mecha cabelo",[(-.46+side*.13+spread,-.25,2.74),
                        (xx+spread,-.28,2.55),(xx+side*.07+spread,-.15,2.17),
                        (xx+side*.11+spread,-.1,1.75),
                        (xx+side*.14+spread,-.16,1.35+ j*.02)],
        .054 if j%2 else .06,brown if j%3 else hairlight,parent=head)
# bangs
for i in range(5):
 start=-.69+i*.12
 curve("franja 3D",[(start,-.28,2.74),(start+.12,-.52,2.67),(start+.2,-.57,2.57)],
       .065,brown if i%3 else hairlight,parent=head)
uv("orelha 1",(-.91,-.23,2.20),(.08,.10,.15),skin,parent=head)
uv("orelha 2",(-.01,-.23,2.20),(.08,.10,.15),skin,parent=head)
# Face eyes oriented forward -Y
eyes=[]
for sx in [-.19,.19]:
 x=-.46+sx
 uv("esclera", (x,-.601,2.35),(.147,.065,.174),white,parent=head)
 uv("iris castanha",(x,-.661,2.35),(.091,.038,.115),iris,parent=head)
 uv("pupila",(x,-.693,2.35),(.056,.022,.078),dark,parent=head)
 uv("brilho olho",(x-.025,-.716,2.40),(.026,.014,.035),white,parent=head)
 blink=uv("palpebra animada",(x,-.72,2.36),(.155,.02,.006),skin,parent=head)
 eyes.append(blink)
 curve("sobrancelha",[(x-.115,-.615,2.57),(x,-.649,2.61),(x+.11,-.619,2.56)],.02,brown,parent=head)
uv("nariz",(-.46,-.637,2.18),(.070,.105,.094),skin,parent=head)
mouth=uv("boca animada",(-.46,-.648,2.035),(.128,.026,.022),pink,parent=head)
uv("luz labio",(-.46,-.678,2.027),(.06,.014,.011),white,parent=head)
# Shoulder rig via articulated arm segments (mesh transforms are keyframed)
left=empty("RIG: braco aponta",(-.91,-.08,1.47),root)
uv("braco esquerdo",(-1.13,-.25,1.18),(.18,.18,.42),black,parent=left)
uv("mao esquerda",(-1.34,-.42,1.03),(.18,.10,.18),skin,parent=left)
curve("dedo aponta",[(-1.39,-.50,1.05),(-1.47,-.56,1.15),(-1.49,-.53,1.30)],.041,skin,parent=left)
right=empty("RIG: braco celular",(.00,-.08,1.47),root)
uv("braco direito",(.22,-.33,1.12),(.18,.19,.37),black,parent=right)
uv("mao direita",(.31,-.46,1.15),(.16,.11,.15),skin,parent=right)
phone=empty("CELULAR RIG",(.48,-.59,1.42),right)
cube("corpo celular",(.48,-.59,1.42),(.51,.10,.80),dark,.065,parent=phone)
cube("tela smartphone",(.48,-.663,1.42),(.445,.018,.69),navy,.025,parent=phone)
text3d("titulo wifi","WI-FI",( .32,-.681,1.66),.095,white,parent=phone)
cube("rede legitima",(.49,-.689,1.50),(.39,.009,.10),cyan,.015,parent=phone)
cube("rede suspeita",(.49,-.689,1.33),(.39,.009,.10),red,.015,parent=phone)
text3d("wifi 1","CAFE",( .30,-.702,1.46),.072,dark,parent=phone)
text3d("wifi 2","GRATIS?",( .30,-.702,1.30),.063,white,parent=phone)
# Animated phone warning: 3D alert icon
warning=uv("alerta vermelho",(.99,-.65,1.66),(.11,.03,.11),red,parent=root)
# Camera and framing. The camera genuinely travels through 3d space.
bpy.ops.object.camera_add(location=(.1,-7.0,2.00))
cam=bpy.context.object;cam.name="camera animada";sc.camera=cam
cam.data.type="ORTHO";cam.data.ortho_scale=3.6
point_cam(cam,(-.38,-.08,1.55))
# lights used in color workbench still geometry receives shading
for pos, energy,color in [((-2,-3,4),1100,(1,.38,.62)),((2,-1,3.5),1500,(.19,.82,1))]:
 ld=bpy.data.lights.new("neon key","AREA");ob=bpy.data.objects.new("light",ld);sc.collection.objects.link(ob)
 ob.location=pos;ld.energy=energy;ld.color=color
# animation timings
frames=[1,max(2,int(N*.25)),max(3,int(N*.52)),max(4,int(N*.75)),N]
poses=[(.10,-6.7,2.12),(.65,-5.0,2.08),(.62,-4.55,1.87),(.02,-6.45,2.12),(.20,-6.7,2.09)]
key(cam,"location",frames,poses)
key(cam,"lens",frames,[3.6,3.4,3.18,3.6,3.4])
for fr in frames:
 cam.location=poses[frames.index(fr)]
 point_cam(cam,(-.30,-.12,1.60))
 cam.keyframe_insert(data_path="rotation_euler",frame=fr)
# body rhythmic movement and head expression/turn
key(root,"location",frames,[(-.46,-.14,0),(-.46,-.14,.015),(-.46,-.14,-.01),(-.46,-.14,.014),(-.46,-.14,0)])
key(head,"rotation_euler",frames,[(0,0,0),(.07,-.08,.05),(-.03,.06,-.05),(.03,-.06,.03),(0,0,0)])
key(left,"rotation_euler",frames,[(0,0,.1),(.13,.08,-.14),(-.21,.03,.24),(-.11,0,.05),(0,0,.14)])
key(right,"rotation_euler",frames,[(0,0,.03),(.08,-.05,-.06),(.18,.06,-.02),(.04,.01,.01),(0,0,.02)])
key(phone,"rotation_euler",frames,[(0,0,-.09),(.07,-.08,.07),(-.05,.1,.16),(0,0,-.05),(0,0,-.09)])
for i in range(1,N+1,3):
 mouth.scale=(.128,.026,.015 + .057*abs(math.sin(i*.82)))
 mouth.keyframe_insert(data_path="scale",frame=i)
for eye in eyes:
 for t in [int(N*.24),int(N*.62),int(N*.88)]:
  for f,val in [(t-2,.006),(t,.19),(t+2,.006)]:
   eye.scale=(.155,.02,val)
   eye.keyframe_insert(data_path="scale",frame=max(1,min(N,f)))
for i in range(1,N+1,6):
 warning.scale=(.11+ .04*abs(math.sin(i*.4)),.03,.11+.04*abs(math.sin(i*.4)))
 warning.keyframe_insert(data_path="scale",frame=i)
# linear interpolation for active moves, smoother for overall motion
for ob in [root,head,left,right,phone,cam,mouth,*eyes,warning]:
 if ob.animation_data and ob.animation_data.action:
  for fc in ob.animation_data.action.fcurves:
   for kp in fc.keyframe_points: kp.interpolation="BEZIER"

# one full test frame helpful when checking execution; whole animation renders to PNG sequence
print("PILOT_3D_SCENE",N,"frames",flush=True)
bpy.ops.render.render(animation=True)
print("PILOT_3D_FRAMES_DONE",N,flush=True)
