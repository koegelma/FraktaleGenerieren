import bpy
import math
import mathutils
from mathutils import Color
import random


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)


def createCube():
    
    for i in range (200):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i/2, math.sin(i*2)*5, 0), scale=(1, 1, 1))
        cube = bpy.context.object
        
        object_color = Color()
        object_color.hsv = (random.uniform(0.28, 0.55), random.uniform(0.9, 1.0), random.uniform(0, 1))
        
        cube.color = (object_color.r, object_color.g, object_color.b, 1)

        currentmesh = bpy.context.object.data


        for vert in currentmesh.vertices:
            angle = math.radians((vert.co.z + 1) * 45)
            
            x = vert.co.x * math.cos(angle) - vert.co.y * math.sin(angle)
            y = vert.co.x * math.sin(angle) + vert.co.y * math.cos(angle)
    
    vert.co.x = x
    vert.co.y = y
    currentmesh.update()




createCube()