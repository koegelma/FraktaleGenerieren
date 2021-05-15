import bpy
import math
import mathutils
from mathutils import Color
import random

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def createCube(cSize): 
    bpy.ops.mesh.primitive_cube_add(size=cSize, location=(0, 0, 0), scale=(1, 1, 1))
    

def iterateCube(iterations):
    
    for iteration in range(iterations):
        cubeSize = bpy.context.object.dimensions[0]

        for i1 in range(3):

            if i1 !=1:
                
                for i in range(2):
                    bpy.ops.object.duplicate()
                    bpy.context.object.location =  (bpy.context.object.location.x + cubeSize, bpy.context.object.location.y, i1 * cubeSize)

                for i in range(2):
                    bpy.ops.object.duplicate()
                    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y + cubeSize, i1 * cubeSize)

                for i in range(2):
                    bpy.ops.object.duplicate()
                    bpy.context.object.location =  (bpy.context.object.location.x - cubeSize, bpy.context.object.location.y, i1 * cubeSize)

                for i in range(2):
                    bpy.ops.object.duplicate()
                    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y - cubeSize, i1 * cubeSize)

        bpy.ops.object.duplicate()
        bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y, bpy.context.object.location.z - cubeSize)

        bpy.ops.object.duplicate()
        bpy.context.object.location =  (bpy.context.object.location.x + cubeSize*2, bpy.context.object.location.y, bpy.context.object.location.z)

        bpy.ops.object.duplicate()
        bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y + cubeSize*2, bpy.context.object.location.z)

        bpy.ops.object.duplicate()
        bpy.context.object.location =  (bpy.context.object.location.x - cubeSize*2, bpy.context.object.location.y, bpy.context.object.location.z)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.join()
        for i in range(iterations):
            dimensions = bpy.context.object.dimensions
            bpy.context.object.dimensions = dimensions[0] / 3, dimensions[1] / 3, dimensions[2] / 3
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        bpy.context.object.location = (0,0,0)
        bpy.ops.object.transform_apply(scale=True)

    

createCube(5)
iterateCube(3)