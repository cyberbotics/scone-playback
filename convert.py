from xml.dom import minidom
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial.transform import Rotation


def add_shape(filename):
    global id

    # if filename[-9:] == 'femur.vtp' or filename[-13:] == 'hat_skull.vtp':
    #     baseColor = " baseColor='1 0.5 0.5'"
    # elif filename[-9:] == 'tibia.vtp':
    #     baseColor = " baseColor='0.5 1 0.5'"
    # else:

    baseColor = ''
    shape = f"<Shape id='n{id}' castShadows='true'>"
    id += 1
    webots = True
    if webots:
        shape += f"""<PBRAppearance id='n{id}' roughness='1' metalness='0' normalMapFactor='0.2'{baseColor}>
<ImageTexture id='n{id+1}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_base_color.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='baseColor'>
<TextureProperties id='n{id+2}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+3}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_roughness.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='roughness'>
<TextureProperties id='n{id+4}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+5}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_normal.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='normal'>
<TextureProperties id='n{id+6}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+7}'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_occlusion.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='occlusion'>
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
    translation = [transform['translation'][0] + transform['tx_default'],
                   transform['translation'][1] + transform['ty_default'],
                   transform['translation'][2] + transform['tz_default']]
    rotation = [transform['rotation'][0],
                transform['rotation'][1],
                transform['rotation'][2],
                transform['rotation'][3]]
    x3d = f"<Transform id='n{transform['id']}' name='{transform['body']}'" + \
          f" translation='{translation[0]} {translation[1]} {translation[2]}'" + \
          f" rotation='{rotation[0]} {rotation[1]} {rotation[2]} {rotation[3]}'>"
    x3d += transform['content']
    print(transform['body'] + ' -> ' + transform['parent_body'])
    x3d += '</Transform>'
    return x3d


# parse an xml file by name
file = open('resources/models/gait0914.osim', 'r')
content = file.read()
file.close()

file = minidom.parseString(content.replace('::', ''))

bodies = file.getElementsByTagName('Body')

x3d = """<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE X3D PUBLIC 'ISO//Web3D//DTD X3D 3.0//EN' 'http://www.web3d.org/specifications/x3d-3.0.dtd'>
<X3D version='3.0' profile='Immersive' xmlns:xsd='http://www.w3.org/2001/XMLSchema-instance'
 xsd:noNamespaceSchemaLocation='http://www.web3d.org/specifications/x3d-3.0.xsd'>
<head>
<meta name='generator' content='Webots' />
</head>
<Scene>
<WorldInfo id='n1' title='Human Skeleton' info='Imported from OpenSim' basicTimeStep='32' coordinateSystem='ENU'>
</WorldInfo>
<Viewpoint id='n2' orientation='0 0 1 3.66' position='12.858 1.682 0.863'
 exposure='1' bloomThreshold='21' zNear='0.05' zFar='0' followSmoothness='0.5' ambientOcclusionRadius='2' followedId='n230'>
</Viewpoint>
<Background id='n3'
 rightUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_right.png'
 rightIrradianceUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_right.hdr'
 leftUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_left.png'
 leftIrradianceUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_left.hdr'
 topUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_top.png'
 topIrradianceUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_top.hdr'
 bottomUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_bottom.png'
 bottomIrradianceUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_bottom.hdr'
 frontUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_front.png'
 frontIrradianceUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_front.hdr'
 backUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_back.png'
 backIrradianceUrl='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_back.hdr'>
</Background>
<DirectionalLight id='n4' direction='0.55 -0.6 -1' intensity='2.7' ambientIntensity='1' castShadows='true'>
</DirectionalLight>
<Transform id='n5' name='rectangle arena' type='solid' translation="5 0 0">
<Shape id='n6' castShadows='false'>
<PBRAppearance id='n7' roughness='1' metalness='0'>
<ImageTexture id='n8'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_base_color.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='baseColor'>
<TextureProperties anisotropicDegree="8" generateMipMaps="true" minificationFilter="AVG_PIXEL"
 magnificationFilter="AVG_PIXEL"/>
</ImageTexture>
<ImageTexture id='n9'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_roughness.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='roughness'>
<TextureProperties anisotropicDegree="8" generateMipMaps="true" minificationFilter="AVG_PIXEL"
 magnificationFilter="AVG_PIXEL"/>
</ImageTexture>
<ImageTexture id='n10'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_normal.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='normal'>
<TextureProperties anisotropicDegree="8" generateMipMaps="true" minificationFilter="AVG_PIXEL"
 magnificationFilter="AVG_PIXEL"/>
</ImageTexture>
<ImageTexture id='n11'
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_occlusion.jpg'
 containerField='' origChannelCount='3' isTransparent='false' role='occlusion'>
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
<Transform id='n13' type='solid' rotation='1 0 0 1.5708'>
"""
id = 14
transforms = []
for body in bodies:
    parent_bodies = body.getElementsByTagName('parent_body')
    if not parent_bodies:
        continue
    transform = {
        "id": id,
        "parent_body": parent_bodies[0].firstChild.data,
        "body": body.attributes['name'].value,
        "mass_center": [float(x) for x in body.getElementsByTagName('mass_center')[0].firstChild.data.split()],
        "translation": [float(x) for x in body.getElementsByTagName('location_in_parent')[0].firstChild.data.split()],
        "rotation": [0, 0, 1, 0],
        "content": '',
        "tx": None,
        "tx_default": 0.0,
        "ty": None,
        "ty_default": 0.0,
        "tz": None,
        "tz_default": 0.0,
        "rx": None,
        "rx_default": 0.0,
        "ry": None,
        "ry_default": 0.0,
        "rz": None,
        "rz_default": 0.0
    }
    id += 1
    transforms.append(transform)
    coordinates = body.getElementsByTagName('Coordinate')
    for coordinate in coordinates:
        motion_type = coordinate.getElementsByTagName('motion_type')[0].firstChild.data
        default_value = float(coordinate.getElementsByTagName('default_value')[0].firstChild.data)
        transform_axes = body.getElementsByTagName('TransformAxis')
        for transform_axis in transform_axes:
            cs = transform_axis.getElementsByTagName('coordinates')[0].firstChild
            if not cs:
                continue
            c = cs.data
            if c != coordinate.attributes['name'].value:
                continue
            value = default_value
            function = transform_axis.getElementsByTagName('function')[0]
            if function:
                constant_tags = function.getElementsByTagName('Constant')
                if len(constant_tags) > 0:
                    value_tag = constant_tags[0].getElementsByTagName('value')[0]
                    if value_tag:
                        value += float(value_tag.firstChild.data)
                simm_spline_tags = function.getElementsByTagName('SimmSpline')
                if len(simm_spline_tags) > 0:
                    x_array = [float(x) for x in simm_spline_tags[0].getElementsByTagName('x')[0].firstChild.data.split()]
                    y_array = [float(y) for y in simm_spline_tags[0].getElementsByTagName('y')[0].firstChild.data.split()]
                    cs = CubicSpline(x_array, y_array)
                    value = cs(default_value)
                    print("cubic spline for " + body.attributes['name'].value + " (" +
                          transform_axis.attributes['name'].value + "): " + str(default_value) + " => " + str(value))
            axis = transform_axis.getElementsByTagName('axis')[0].firstChild.data
            name = transform_axis.attributes['name'].value
            if name == 'translation1':
                transform['tx'] = c
                transform['tx_default'] = value
            elif name == 'translation2':
                transform['ty'] = c
                transform['ty_default'] = value
            elif name == 'translation3':
                transform['tz'] = c
                transform['tz_default'] = value
            elif name == 'rotation1':
                transform['rx'] = c
                transform['rx_default'] = value
            elif name == 'rotation2':
                transform['ry'] = c
                transform['ry_value'] = value
            elif name == 'rotation3':
                transform['rz'] = c
                transform['rz_value'] = value
            else:
                print('Wrong TranformAxis name: ' + name)
    geometry_files = body.getElementsByTagName('geometry_file')
    for geometry_file in geometry_files:
        transform['content'] += add_shape('resources/geometry/' + geometry_file.firstChild.data)

muscles = file.getElementsByTagName('Millard2012EquilibriumMuscle')
muscle_count = 0
for muscle in muscles:
    print('Muscle: ' + muscle.attributes['name'].value)
    path_points = muscle.getElementsByTagName('PathPoint') + muscle.getElementsByTagName('MovingPathPoint')
    for i in [0, len(path_points) - 1]:
        path_point = path_points[i]
        location = path_point.getElementsByTagName('location')[0].firstChild.data.strip()
        body = path_point.getElementsByTagName('body')[0].firstChild.data
        content = f"\n<Transform id='n{id}' translation='{location}'><Shape id='n{id + 1}' castShadows='true'>\n"
        base_color = '1 0.54 0.08' if i == 0 else '0.54 1 0.08'
        content += f"  <PBRAppearance id='n{id + 2}' baseColor='{base_color}' roughness='0.3' metalness='0'></PBRAppearance>\n"
        content += f"  <Sphere id='n{id + 3}' radius='0.0325'></Sphere>\n</Shape></Transform>\n"
        id += 4
        sphere = {
                "id": id,
                "parent_body": body,
                "body": f"muscle-{muscle_count}",
                "translation": [0, 0, 0],
                "rotation": [1, 0, 0, 0],
                "content": content,
                "tx": None,
                "tx_default": 0.0,
                "ty": None,
                "ty_default": 0.0,
                "tz": None,
                "tz_default": 0.0,
                "rx": None,
                "rx_default": 0.0,
                "ry": None,
                "ry_default": 0.0,
                "rz": None,
                "rz_default": 0.0}
        id += 1
        muscle_count += 1
        transforms.append(sphere)
        print(f'{body}: {location}')

for transform in transforms:  # adding transforms to X3D
    x3d += add_transform(transform)

x3d += '</Transform>\n'
x3d += '</Scene></X3D>\n'

file = open('model.x3d', 'w')
file.write(x3d)
file.close()

# generate the animation file from the STO file


def list_bodies(bones, muscles, t):
    if t['body'].startswith('muscle-'):
        muscles.append(t)
    else:
        bones.append(t)


bones = []
muscles = []
for transform in transforms:
    list_bodies(bones, muscles, transform)
bodies = bones + muscles

print([x['body'] for x in bodies])

file = open('resources/sto/1704_0.526_0.519.par.sto')
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
count = 0
for line in lines:
    time = int(line[0] * 1000)
    animation += f'{{"time":{time},"poses":['
    for bone in bones:
        name = bone['body']
        id = bone['id']
        tx = header.index(name + '.com_pos_x')
        ty = header.index(name + '.com_pos_y')
        tz = header.index(name + '.com_pos_z')
        rx = header.index(name + '.ori_x')
        ry = header.index(name + '.ori_y')
        rz = header.index(name + '.ori_z')
        r = Rotation.from_euler('xyz', [line[rx], line[ry], line[rz]])
        rotvec = r.as_rotvec()
        angle = np.linalg.norm(rotvec)
        animation += f'{{"id":{id},'
        x = line[tx]
        y = line[ty]
        z = line[tz]
        r2 = r.apply(bone['mass_center'])
        x -= r2[0]
        y -= r2[1]
        z -= r2[2]
        animation += f'"translation":"{x} {y} {z}",'
        animation += f'"rotation":"{rotvec[0]/angle} {rotvec[1]/angle} {rotvec[2]/angle} {angle}"}},'
        for muscle in muscles:
            if muscle['parent_body'] == name:
                id = muscle['id']
                animation += f'{{"id":{id},'
                animation += f'"translation":"{x} {y} {z}"}},'
    animation = animation[:-1]  # remove final coma
    animation += ']},'
    count += 1
animation = animation[:-1] + ']}\n'
file = open('animation.json', 'w', newline='\n')
file.write(animation)
file.close()
