from xml.dom import minidom


def add_geometry(filename):
    file = minidom.parse(filename)
    normals = file.getElementsByTagName('PointData')[0].getElementsByTagName('DataArray')[0]
    vertices = file.getElementsByTagName('Points')[0].getElementsByTagName('DataArray')[0]
    indices = file.getElementsByTagName('Polys')[0].getElementsByTagName('DataArray')[0]
    geometry = '<IndexedFaceSet coordIndex="'
    for line in indices.firstChild.data.splitlines():
        line = line.strip()
        if not line:
            continue
        geometry += line + ' -1 '
    geometry = geometry[:-1]  # remove final space
    geometry += '">\n<Coordinate point="'
    for line in vertices.firstChild.data.splitlines():
        line = line.strip()
        if not line:
            continue
        geometry += line + ' '
    geometry = geometry[:-1]  # remove final space
    geometry += '">\n<Normal vector="'
    for line in normals.firstChild.data.splitlines():
        line = line.strip()
        if not line:
            continue
        geometry += line + ' '
    geometry = geometry[:-1]  # remove final space
    geometry += '">\n</IndexeFaceSet>'
    return geometry


# parse an xml file by name
file = open('resources/models/gait0914.osim', 'r')
content = file.read()
file.close()

file = minidom.parseString(content.replace('::', ''))

bodies = file.getElementsByTagName('Body')

x3d = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.0//EN" "http://www.web3d.org/specifications/x3d-3.0.dtd">
<x3d version="3.0" profile="Immersive" xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"
 xsd:noNamespaceSchemaLocation="http://www.web3d.org/specifications/x3d-3.0.xsd">
<head>
<meta name="generator" content="Webots" />
</head>
<Scene>
<WorldInfo id='n1' docUrl='https://cyberbotics.com/doc/reference/worldinfo' title="" info='' basicTimeStep='32'
 coordinateSystem='ENU'>
</WorldInfo>
<Viewpoint id='n2' docUrl='https://cyberbotics.com/doc/reference/viewpoint'
 orientation='-0.23244937 -0.14943881 0.9610595 3.9676616' position='0.24667683 0.30063453 0.22481202' exposure='1'
 bloomThreshold='21' zNear='0.05' zFar='0' followSmoothness='0.5' ambientOcclusionRadius='2' followedId='n230'>
</Viewpoint>
<Background id='n3' docUrl='https://cyberbotics.com/doc/guide/object-backgrounds'
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
<DirectionalLight id='n4' docUrl='https://cyberbotics.com/doc/guide/object-backgrounds' direction='0.55 -0.6 -1'
 intensity='2.7' ambientIntensity='1' castShadows='TRUE'>
</DirectionalLight>
'''

id = 10

for body in bodies:
    x3d += f"<Transform id='n{id}' name='{body.attributes['name'].value}'><Shape castShadows='true'>"
    x3d += """
<PBRAppearance roughness='1' metalness='0'>
<ImageTexture
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_base_color.jpg'
 containerField='' origChannelCount='3' isTransparent='false' type='baseColor'>
<TextureProperties anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_roughness.jpg'
 containerField='' origChannelCount='3' isTransparent='false' type='roughness'>
<TextureProperties anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_normal.jpg'
 containerField='' origChannelCount='3' isTransparent='false' type='normal'>
<TextureProperties anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter='AVG_PIXEL'/>
</ImageTexture>
<ImageTexture
 url='https://raw.githubusercontent.com/cyberbotics/webots/R2022a/projects/appearances/protos/textures/parquetry/chequered_parquetry_occlusion.jpg'
 containerField='' origChannelCount='3' isTransparent='false' type='occlusion'>
<TextureProperties anisotropicDegree='8' generateMipMaps='true' minificationFilter='AVG_PIXEL'
 magnificationFilter="AVG_PIXEL"/>
</ImageTexture>
</PBRAppearance>"""
    id += 1
    geometry_files = body.getElementsByTagName('geometry_file')
    for geometry_file in geometry_files:
        x3d += add_geometry('resources/geometry/' + geometry_file.firstChild.data)
    x3d += '</Shape></Transform>\n'
x3d += '</Scene></x3d>\n'

file = open('model.x3d', 'w')
file.write(x3d)
file.close()
