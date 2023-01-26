# 14 muscles
#  Millard
#   Geyer2010
#    => gait0914.osim + geyer_14.sto
#   spinal_controller
#    => gait0914.osim + geyer_spinal_controller_14.sto
# 18 muscle
#  Millard
#   Ong2019
#    => gait0918_millard.osim + Millard_ong_18.sto
#   spinal_controller
#    => gait0918_millard.osim + Millard_spinal_controller_18.sto
#  Thelen
#   Ong2019
#    => gait9dof18musc_Thelen_20170320.osim + Thelen_ong_18.sto
#   spinal_controller
#    => gait9dof18musc_Thelen_20170320.osim + ong_spinal_controller.sto

from xml.dom import minidom
import numpy as np
from scipy.spatial.transform import Rotation


def list_bodies(bones, muscles, t):
    if t['body'].startswith('muscle-'):
        muscles.append(t)
    elif not t['body'].startswith('tendon-'):
        bones.append(t)


def add_shape(filename):
    global id

    baseColor = ''
    shape = f"<Shape id='n{id}' castShadows='true'>"
    id += 1
    webots = True
    if webots:
        shape += f"""<PBRAppearance id='n{id}' roughness='1' metalness='0' normalMapFactor='0.2'{baseColor}>
<ImageTexture id='n{id+1}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_base_color.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='baseColorMap'>
<TextureProperties id='n{id+2}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+3}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_roughness.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='roughnessMap'>
<TextureProperties id='n{id+4}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+5}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_normal.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='normalMap'>
<TextureProperties id='n{id+6}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+7}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_occlusion.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='occlusionMap'>
<TextureProperties id='n{id+8}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter="AVG_PIXEL"/>
</ImageTexture>
</PBRAppearance>
"""
    id += 9
    file = minidom.parse(filename)
    normals = file.getElementsByTagName('PointData')[0].getElementsByTagName('DataArray')[0]
    vertices = file.getElementsByTagName('Points')[0].getElementsByTagName('DataArray')[0]
    indices = file.getElementsByTagName('Polys')[0].getElementsByTagName('DataArray')[0]
    shape += f"<IndexedFaceSet id='n{id}' coordIndex='"
    id += 1
    index = ''
    for line in indices.firstChild.data.splitlines():
        line = ' '.join(line.split())
        if not line:
            continue
        indices = line.split()
        length = len(indices) - 2
        for i in range(length):  # assuming convex faces
            index += indices[0] + ' ' + indices[i+1] + ' ' + indices[i+2] + ' -1 '
    index = index[:-1]  # remove final space
    shape += index + "' normalIndex='" + index + "'>\n"
    shape += f"<Coordinate id='n{id}' point='"
    id += 1
    for line in vertices.firstChild.data.splitlines():
        line = ' '.join(line.split())
        if not line:
            continue
        shape += line + ' '
    shape = shape[:-1]  # remove final space
    shape += f"'></Coordinate>\n<Normal id='n{id}' vector='"
    id += 1
    for line in normals.firstChild.data.splitlines():
        line = line.strip()
        if not line:
            continue
        shape += line + ' '
    shape = shape[:-1]  # remove final space
    shape += "'></Normal>\n"
    shape += "</IndexedFaceSet></Shape>"
    return shape


def add_transform(transform):
    x3d = f"<Transform id='n{transform['id']}' name='{transform['body']}'"
    if 'location_in_parent' in transform:
        translation = [transform['location_in_parent'][0],
                       transform['location_in_parent'][1],
                       transform['location_in_parent'][2]]
        if translation != [0, 0, 0]:
            x3d += f" translation='{translation[0]} {translation[1]} {translation[2]}'"
    x3d += '>'
    x3d += transform['content']
    x3d += '</Transform>'
    return x3d


def compute_transform(line, header, name, mass_center, offset=[0, 0, 0]):
    tx = header.index(name + '.com_pos_x')
    ty = header.index(name + '.com_pos_y')
    tz = header.index(name + '.com_pos_z')
    ox = header.index(name + '.ori_x')
    oy = header.index(name + '.ori_y')
    oz = header.index(name + '.ori_z')
    r = Rotation.from_euler('xyz', [line[ox], line[oy], line[oz]])
    rotvec = r.as_rotvec()
    r2 = r.apply(mass_center)
    angle = np.linalg.norm(rotvec)
    rx = rotvec[0]/angle
    ry = rotvec[1]/angle
    rz = rotvec[2]/angle
    x = line[tx] + offset[0] - r2[0]
    y = line[ty] + offset[1] - r2[1]
    z = line[tz] + offset[2] - r2[2]
    return [x, y, z, rx, ry, rz, angle]


def compute_position(line, header, name, mass_center, offset):
    tx = header.index(name + '.com_pos_x')
    ty = header.index(name + '.com_pos_y')
    tz = header.index(name + '.com_pos_z')
    ox = header.index(name + '.ori_x')
    oy = header.index(name + '.ori_y')
    oz = header.index(name + '.ori_z')
    r = Rotation.from_euler('xyz', [line[ox], line[oy], line[oz]])
    r2 = r.apply(mass_center)
    r3 = r.apply(offset)
    x = line[tx] + r3[0] - r2[0]
    y = line[ty] + r3[1] - r2[1]
    z = line[tz] + r3[2] - r2[2]
    return [x, y, z]


# parse an xml file by name
file = open('resources/models/gait9dof18musc_Thelen_20170320.osim', 'r')
content = file.read()
file.close()

file = minidom.parseString(content.replace('::', ''))

bones = file.getElementsByTagName('Body')

x3d = """<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE X3D PUBLIC 'ISO//Web3D//DTD X3D 3.0//EN' 'http://www.web3d.org/specifications/x3d-3.0.dtd'>
<X3D version='3.0' profile='Immersive' xmlns:xsd='http://www.w3.org/2001/XMLSchema-instance'
 xsd:noNamespaceSchemaLocation='http://www.web3d.org/specifications/x3d-3.0.xsd'>
<head>
<meta name='generator' content='Webots' />
<meta name='version' content='R2022b' />
</head>
<Scene>
<WorldInfo id='n1' title='Human Skeleton' info='Imported from OpenSim' basicTimeStep='32' coordinateSystem='ENU'>
</WorldInfo>
<Viewpoint id='n2' orientation='0 0 1 3.66' position='12.858 1.682 0.863'
 exposure='1' bloomThreshold='21' zNear='0.05' zFar='0' followSmoothness='0.5' ambientOcclusionRadius='2' followedId='n230'>
</Viewpoint>
<Background id='n3' skyColor='0.7 0.7 0.7' luminosity='0.8'>
</Background>
<DirectionalLight id='n4' direction='0.55 -0.6 -1' intensity='2.7' ambientIntensity='1' castShadows='true'>
</DirectionalLight>
<Transform id='n5' name='rectangle arena' type='solid' translation="5 0 0">
<Shape id='n6' castShadows='false'>
<PBRAppearance id='n7' roughness='1' metalness='0' baseColor='0.8 0.8 0.8'>
<ImageTexture id='n8'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/grid.png'
 containerField='' origChannelCount='3' isTransparent='false' role='baseColorMap'>
<TextureProperties anisotropicDegree="8" generateMipMaps="true" minificationFilter="AVG_PIXEL"
 magnificationFilter="AVG_PIXEL"/>
</ImageTexture>
</PBRAppearance>
<IndexedFaceSet id='n12' coordIndex='0 1 2 -1 1 0 3 -1' normalIndex='0 0 0 -1 0 0 0 -1' texCoordIndex='0 1 2 -1 1 0 3 -1'>
<Coordinate point='10.0000 -10.0000 0.0000, -10.0000 10.0000 0.0000, -10.0000 -10.0000 0.0000, 10.0000 10.0000 0.0000'>
</Coordinate>
<Normal vector='0.0000 0.0000 1.0000'></Normal>
<TextureCoordinate point='16.0000 0.0000, 0.0000 16.0000, 0.0000 0.0000, 16.0000 16.0000'></TextureCoordinate>
</IndexedFaceSet>
</Shape></Transform>
<Transform id='n13' type='solid' name='skeleton' rotation='1 0 0 1.5708'>
"""
id = 14
transforms = []
for bone in bones:
    parent_bodies = bone.getElementsByTagName('parent_body')
    if not parent_bodies:
        continue
    transform = {
        "id": id,
        "parent_body": parent_bodies[0].firstChild.data,
        "body": bone.attributes['name'].value,
        "mass_center": [float(x) for x in bone.getElementsByTagName('mass_center')[0].firstChild.data.split()],
        "location_in_parent": [float(x) for x in bone.getElementsByTagName('location_in_parent')[0].firstChild.data.split()],
        "content": ''}
    id += 1
    transforms.append(transform)
    geometry_files = bone.getElementsByTagName('geometry_file')
    for geometry_file in geometry_files:
        transform['content'] += add_shape('resources/geometry/' + geometry_file.firstChild.data)

muscles = file.getElementsByTagName('Millard2012EquilibriumMuscle') + file.getElementsByTagName('Thelen2003Muscle')
for muscle in muscles:
    max_isometric_force = float(muscle.getElementsByTagName('max_isometric_force')[0].firstChild.data)
    tendon_slack_length = float(muscle.getElementsByTagName('tendon_slack_length')[0].firstChild.data)
    path_points = muscle.getElementsByTagName('PathPoint') + muscle.getElementsByTagName('MovingPathPoint')
    last = len(path_points) - 1
    radius = max_isometric_force / 1000000
    name = muscle.attributes['name'].value
    start_location = path_points[0].getElementsByTagName('location')[0].firstChild.data.strip()
    end_location = path_points[last].getElementsByTagName('location')[0].firstChild.data.strip()

    # tendon
    content = f"<Shape id='n{id}' castShadows='true'>\n"
    content += f"<PBRAppearance id='n{id + 1}' baseColor='1 0.54 0.08' roughness='0.3' metalness='0'></PBRAppearance>\n"
    content += f"<Capsule id='n{id + 2}' radius='{radius}' height='{tendon_slack_length}'></Capsule>\n</Shape>\n"
    id += 3
    transform = {
      "id": id,
      "body": f"tendon-{name}",
      "content": content
    }
    id += 1
    transforms.append(transform)

    # muscle
    content = f"<Shape id='n{id}' castShadows='true'>\n"
    content += f"<PBRAppearance id='n{id + 1}' baseColor='1 0.2 0.08' roughness='0.3' metalness='0'></PBRAppearance>\n"
    content += f"<Capsule id='n{id + 2}' radius='{radius * 2}' height='{tendon_slack_length / 2}'></Capsule>\n</Shape>\n"
    id += 3
    transform = {
      "id": id,
      "body": f"muscle-{name}",
      "start_bone": path_points[0].getElementsByTagName('body')[0].firstChild.data,
      "start_location": [float(x) for x in start_location.split()],
      "end_bone": path_points[last].getElementsByTagName('body')[0].firstChild.data,
      "end_location": [float(x) for x in end_location.split()],
      "max_isometric_force": max_isometric_force,
      "tendon_slack_length": tendon_slack_length,
      "content": content
    }
    id += 1
    transforms.append(transform)
    print('Muscle: ' + transform['body'] + ' between ' + transform['start_bone'] + ' and ' + transform['end_bone'])

for transform in transforms:  # adding transforms to X3D
    x3d += add_transform(transform)

x3d += '</Transform>\n'
x3d += '</Scene></X3D>\n'

file = open('model.x3d', 'w')
file.write(x3d)
file.close()

# generate the animation file from the STO file

bones = []
muscles = []
for transform in transforms:
    list_bodies(bones, muscles, transform)
bodies = bones + muscles

print([x['body'] for x in bodies])

file = open('resources/sto/ong_spinal_controller.sto')
while True:
    line = file.readline().strip()
    if line == 'endheader':
        break
header = file.readline().split()

lines = []
while True:
    line = file.readline()
    if line:
        lines.append([float(x) for x in line.split()])
    else:
        break
file.close()

basic_time_step = int(lines[1][0] * 1000)
ids = ''
for body in bodies:
    ids += str(body['id']) + ';'
ids = ids[:-1]
animation = f'{{"basicTimeStep":{basic_time_step},"ids":"{ids}","labelsIds":"","frames":['
angles = f'{{"basicTimeStep":{basic_time_step}, "names": ["leg0_l.grf_x", "leg1_r.grf_x", "leg0_l.grf_y", "leg1_r.grf_y", "leg0_l.grf_z", "leg1_r.grf_z", "hamstrings_r.mtu_length", "glut_max_r.mtu_length", "iliopsoas_r.mtu_length",  "vasti_r.mtu_length", "gastroc_r.mtu_length", "soleus_r.mtu_length", "tib_ant_r.mtu_length", "hamstrings_l.mtu_length", "glut_max_l.mtu_length", "iliopsoas_l.mtu_length", "vasti_l.mtu_length", "gastroc_l.mtu_length", "soleus_l.mtu_length", "tib_ant_l.mtu_length","pelvis_tilt", "hip_flexion_r", "knee_angle_r", "ankle_angle_r", "hip_flexion_l", "knee_angle_l", "ankle_angle_l", "hamstrings_r.activation", "glut_max_r.activation", "iliopsoas_r.activation", "vasti_r.activation", "gastroc_r.activation", "soleus_r.activation", "tib_ant_r.activation", "hamstrings_l.activation", "glut_max_l.activation", "iliopsoas_l.activation", "vasti_l.activation", "gastroc_l.activation", "soleus_l.activation", "tib_ant_l.activation"], "frames":['

angles_name = ["leg0_l.grf_x", "leg1_r.grf_x", "leg0_l.grf_y", "leg1_r.grf_y",
 "leg0_l.grf_z", "leg1_r.grf_z", "hamstrings_r.mtu_length", "glut_max_r.mtu_length", "iliopsoas_r.mtu_length",
 "vasti_r.mtu_length", "gastroc_r.mtu_length", "soleus_r.mtu_length", "tib_ant_r.mtu_length", "hamstrings_l.mtu_length",
 "glut_max_l.mtu_length", "iliopsoas_l.mtu_length", "vasti_l.mtu_length", "gastroc_l.mtu_length", "soleus_l.mtu_length",
 "tib_ant_l.mtu_length", "pelvis_tilt", "hip_flexion_r", "knee_angle_r", "ankle_angle_r", "hip_flexion_l", "knee_angle_l",
 "ankle_angle_l", "hamstrings_r.activation", "glut_max_r.activation", "iliopsoas_r.activation", "vasti_r.activation",
 "gastroc_r.activation", "soleus_r.activation", "tib_ant_r.activation", "hamstrings_l.activation", "glut_max_l.activation",
 "iliopsoas_l.activation", "vasti_l.activation", "gastroc_l.activation", "soleus_l.activation", "tib_ant_l.activation"]

count = 0

for line in lines:
    time = int(line[0] * 1000)
    animation += f'{{"time":{time},"updates":['
    for bone in bones:
        name = bone['body']
        id = bone['id']
        transform = compute_transform(line, header, name, bone['mass_center'])
        animation += f'{{"id":{id},'
        animation += f'"translation":"{transform[0]} {transform[1]} {transform[2]}",'
        animation += f'"rotation":"{transform[3]} {transform[4]} {transform[5]} {transform[6]}"}},'
    for muscle in muscles:
        id = muscle['id']
        for bone in bones:
            if muscle['start_bone'] == bone['body']:
                start_position = compute_position(line, header, bone['body'], bone['mass_center'], muscle['start_location'])
            elif muscle['end_bone'] == bone['body']:
                end_position = compute_position(line, header, bone['body'], bone['mass_center'], muscle['end_location'])

        name = muscle['body'][7:]
        activation = line[header.index(name + '.activation')]
        fiber_length = line[header.index(name + '.fiber_length')]
        tendon_length = line[header.index(name + '.tendon_length')]
        mtu_length = line[header.index(name + '.mtu_length')]
        tendon_slack_length = muscle['tendon_slack_length']
        muscle_scale = fiber_length / (tendon_slack_length / 2)
        muscle_color = f'{activation} {0} {1 - activation}'
        v1 = np.array([0, 0, 1])
        v2 = np.array([end_position[0] - start_position[0],
                       end_position[1] - start_position[1],
                       end_position[2] - start_position[2]])
        tendon_scale = mtu_length / tendon_slack_length
        # the value of mtu_length should equal np.linalg.norm(v2)
        cross_product = np.cross(v1, v2)
        axis = cross_product / np.linalg.norm(cross_product)
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        translation = [(start_position[0] + end_position[0]) / 2,
                       (start_position[1] + end_position[1]) / 2,
                       (start_position[2] + end_position[2]) / 2]
        # muscle
        animation += f'{{"id":{id},'
        animation += f'"translation":"{translation[0]} {translation[1]} {translation[2]}",'
        animation += f'"rotation":"{axis[0]} {axis[1]} {axis[2]} {angle}",'
        animation += f'"scale":"1 1 {muscle_scale}"}},'

        # muscle appearance
        animation += f'{{"id":{id - 2},'
        animation += f'"baseColor":"{muscle_color}"}},'

        # tendon
        animation += f'{{"id":{id - 4},'
        animation += f'"translation":"{translation[0]} {translation[1]} {translation[2]}",'
        animation += f'"rotation":"{axis[0]} {axis[1]} {axis[2]} {angle}",'
        animation += f'"scale":"1 1 {tendon_scale}"}},'
    animation = animation[:-1]  # remove final coma
    animation += ']},'

    angles += f'{{"time": {time}, "angles": ' + '{'

    for name in angles_name:
        if (name in ["pelvis_tilt", "knee_angle_l", "knee_angle_r"]):
            value = -1 *line[header.index(name)]
            angles += f'"{name}":{value},'
        else:
            angles += f'"{name}":{line[header.index(name)]},'
    angles = angles[:-1]
    angles += '}},'
    count += 1
animation = animation[:-1] + ']}\n'
file = open('animation.json', 'w', newline='\n')
file.write(animation)
file.close()

angles = angles[:-1] + ']}\n'
file = open('angles.json', 'w', newline='\n')
file.write(angles)
file.close()
