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
        object_color.hsv = (random.uniform(0.03, 0.07), random.uniform(0.4, 0.8), random.uniform(1, 0))
        
        cube.color = (object_color.r, object_color.g, object_color.b, 1)



createCube()