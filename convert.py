from xml.dom import minidom


def add_shape(filename):
    global id

    shape = f"<Shape id='n{id}'>"
    id += 1
    if webots:
        shape += f"""<PBRAppearance id='n{id}' roughness='1' metalness='0' normalMapFactor='0.2'>
<ImageTexture id='n{id+1}'
 url='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_base_color.jpg"'
 containerField='' origChannelCount='3' isTransparent='false' type='baseColor'>
<TextureProperties id='n{id+2}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+3}'
 url='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_roughness.jpg"'
 containerField='' origChannelCount='3' isTransparent='false' type='roughness'>
<TextureProperties id='n{id+4}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture  id='n{id+5}'
 url='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_normal.jpg"'
 containerField='' origChannelCount='3' isTransparent='false' type='normal'>
<TextureProperties id='n{id+6}' anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture id='n{id+7}'
 url='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/marble/marble_occlusion.jpg"'
 containerField='' origChannelCount='3' isTransparent='false' type='occlusion'>
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
        line = line.strip()
        if not line:
            continue
        indices = line.split()
        length = len(indices) - 2
        for i in range(length):  # assuming convex faces
            index += indices[0] + ' ' + indices[i+1] + ' ' + indices[i+2] + ' -1 '
    index = index[:-1]  # remove final space
    shape += index + "' normalIndex='" + index + "'>\n"
    shape += f"'<Coordinate id='n{id}' point='"
    id += 1
    for line in vertices.firstChild.data.splitlines():
        line = line.strip()
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
    global id
    translation = [transform['translation'][0] + transform['tx_default'],
                   transform['translation'][1] + transform['ty_default'],
                   transform['translation'][2] + transform['tz_default']]
    rotation = [transform['rotation'][0],
                transform['rotation'][1],
                transform['rotation'][2],
                transform['rotation'][3]]
    x3d = f"<Transform id='n{id}' name='{transform['body']}'" + \
          f" translation='{translation[0]} {translation[1]} {translation[2]}'" + \
          f" rotation='{rotation[0]} {rotation[1]} {rotation[2]} {rotation[3]}'>"
    id += 1
    x3d += transform['content']
    for child in transform['children']:
        x3d += add_transform(child)
    x3d += '</Transform>'
    return x3d


id = 10
webots = True
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
<WorldInfo id='n1' title='Human Skeleton' info='"Imported from OpenSim"' basicTimeStep='32' coordinateSystem='ENU'>
</WorldInfo>
<Viewpoint id='n2' orientation='0 0 1 4.375' position='1.133 2.733 0.768'
 exposure='1' bloomThreshold='21' zNear='0.05' zFar='0' followSmoothness='0.5' ambientOcclusionRadius='2' followedId='n230'>
</Viewpoint>
<Background id='n3'
 rightUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_right.png"'
 rightIrradianceUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_right.hdr"'
 leftUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_left.png"'
 leftIrradianceUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_left.hdr"'
 topUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_top.png"'
 topIrradianceUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_top.hdr"'
 bottomUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_bottom.png"'
 bottomIrradianceUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_bottom.hdr"'
 frontUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_front.png"'
 frontIrradianceUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_front.hdr"'
 backUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_back.png"'
 backIrradianceUrl='"https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/default/worlds/textures/cubic/mountains_back.hdr"'>
</Background>
<DirectionalLight id='n4' direction='0.55 -0.6 -1' intensity='2.7' ambientIntensity='1'>
</DirectionalLight>
<Transform id='n5' solid='true' rotation='1 0 0 1.5708'>
"""

transforms = []
for body in bodies:
    parent_bodies = body.getElementsByTagName('parent_body')
    if not parent_bodies:
        continue
    location_in_parent = body.getElementsByTagName('location_in_parent')[0].firstChild.data
    t = location_in_parent.split()
    transform = {
        "parent_body": parent_bodies[0].firstChild.data,
        "body": body.attributes['name'].value,
        "translation": [float(t[0]), float(t[1]), float(t[2])],
        "rotation": [0, 0, 1, 0],
        "content": '',
        "children": [],
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
    transforms.append(transform)
    coordinates = body.getElementsByTagName('Coordinate')
    count = 0
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
            axis = transform_axis.getElementsByTagName('axis')[0].firstChild.data
            count += 1
            id += 1
            if motion_type == 'translational':
                if axis == '1 0 0':
                    transform['tx'] = c
                    transform['tx_default'] = default_value
                elif axis == '0 1 0':
                    transform['ty'] = c
                    transform['ty_default'] = default_value
                elif axis == '0 0 1':
                    transform['tz'] = c
                    transform['tz_default'] = default_value
                else:
                    print('Wrong translational axis: ' + axis)
            elif motion_type == 'rotational':
                if axis == '1 0 0':
                    transform['rx'] = c
                    transform['rx_default'] = default_value
                elif axis == '0 1 0':
                    transform['ry'] = c
                    transform['ry_value'] = default_value
                elif axis == '0 0 1':
                    transform['rz'] = c
                    transform['rz_value'] = default_value
                else:
                    print('Wrong rotational axis: ' + axis)
            else:
                print('Wrong motion type: ' + motion_type)
    geometry_files = body.getElementsByTagName('geometry_file')
    for geometry_file in geometry_files:
        transform['content'] += add_shape('resources/geometry/' + geometry_file.firstChild.data)

root = []
for transform in transforms:  # nesting transforms
    if transform['parent_body'] == 'ground':
        root.append(transform)
        print('Adding ' + transform['body'] + ' to ground')
    else:
        for parent in transforms:
            if transform['parent_body'] == parent['body']:
                parent['children'].append(transform)
                print('Adding ' + transform['body'] + ' to ' + parent['body'])

for transform in root:  # adding transforms to X3D
    x3d += add_transform(transform)

x3d += '</Transform>\n'
x3d += '</Scene></X3D>\n'

file = open('model.x3d', 'w')
file.write(x3d)
file.close()
