#REM Python console: blank lines terminate function definition
import bpy
import bmesh
from mathutils import *
from math import *

def expTransform(point):
    z = point[1]
    r = 0.2 + 10.0*exp(-z)
    x = r*sin(point[0])
    y = r*cos(point[0])
    return (x, y, z)

def triple(p):
    u = p[0]
    v = p[1]
    return (3*u, v, 0)

def cylindrical(p):
    u = p[0]
    v = p[1]
    r = 3.0
    return (r*sin(u), r*cos(u), v)

def planePolar(p):
    r = p[0]
    theta = p[1]
    z = 0
    return (r*sin(theta), r*cos(theta), z)

def expSpacing(p):
    u = p[0]
    v = p[1]
    return (u, log(v), 0)
		
def make1DVertexArray(spacing, cols, rows, colOffset, rowOffset):
	vertices = []
	du = spacing[0]
	dv = spacing[1]
	for i in range(cols):
		for j in range(rows):
			vertices.append(((i + colOffset)*du, (j + rowOffset)*dv, 0))
	return vertices

def indexOf(i, j, cols, rows):
	return (i*rows) + j
	
def makeEdgeList(vertexArray, cols, rows, subs):
	edges = []
	for i in range(cols):
		for j in range(rows):
			p0 = indexOf(i, j, cols, rows)
			if (i%subs == 0) and (j < rows - 1):
				p1 = indexOf(i, j + 1, cols, rows)
				edges.append((p0, p1))
			if (j%subs == 0) and (i < cols - 1):
				p1 = indexOf(i + 1, j, cols, rows)
				edges.append((p0, p1))
	return edges
	
def transformedVertexList(spacing, cols, rows, colOffset, rowOffset, transform):
	vertices = make1DVertexArray(spacing, cols, rows, colOffset, rowOffset)
	for i in range(len(vertices)):
		vertices[i] = transform(vertices[i])
	return vertices

#cols should be multiple of subs for circular
subs = 5

colOffset = 0
rowOffset = 0


cols = 101
rows = 201
spacing = ((2.0*pi)/(cols - 1). 1.0)
transform = cylindrical

vertices = transformedVertexList(spacing, cols, rows, \
    colOffset, rowOffset, transform)
edges = makeEdgeList(vertices, cols, rows, subs)

verts_mesh = bpy.data.meshes.new("verts")
verts_object = bpy.data.objects.new("verts", verts_mesh)
verts_object.location = (0, 0, 0)
bpy.context.scene.objects.link(verts_object)
verts_mesh.from_pydata(vertices, edges, [])
verts_mesh.update()

wire = bpy.data.materials.new(name="Wire")
wire.type = 'WIRE'
wire.emit = 1.2
if verts_object.data.materials:
    verts_object.data.materials[0] = wire
else:
    verts_object.data.materials.append(wire)