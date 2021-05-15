import bpy
import math
import mathutils
from mathutils import Color
import random

#TODO 
# - Definition von cube als Objekt stimmt noch nicht, bzw. die Selektion als ausgewähltes Objekt (obj.select_set(True))
# - join usw. nach lastIteration wird nicht ausgeführt


cubeList = []

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def createCube(cSize): 
    bpy.ops.mesh.primitive_cube_add(size=cSize, location=(0, 0, 0), scale=(1, 1, 1))


def duplicate(cube):
    # Definition von cube als Objekt stimmt noch nicht, bzw. die Selektion als ausgewähltes Objekt (obj.select_set(True))
    tempCube: bpy.types.Object = cube
    tempCube.select_set(True)
    bpy.context.view_layer.objects.active = tempCube
    bpy.ops.object.duplicate()
    dimensions = bpy.context.object.dimensions
    bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2


def createIterationRemaining(cube):
    # Definition von cube als Objekt stimmt noch nicht, bzw. die Selektion als ausgewähltes Objekt (obj.select_set(True))
    tempCube: bpy.types.Object = cube
    tempCube.select_set(True)
    bpy.context.view_layer.objects.active = tempCube
    cubeSize = bpy.context.object.dimensions[0] * 3/4

    cubeList.append(duplicate(tempCube))
    bpy.context.object.location =  (bpy.context.object.location.x + cubeSize, bpy.context.object.location.y, bpy.context.object.location.z)

    cubeList.append(duplicate(tempCube))
    bpy.context.object.location =  (bpy.context.object.location.x - cubeSize, bpy.context.object.location.y, bpy.context.object.location.z)

    cubeList.append(duplicate(tempCube))
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y + cubeSize, bpy.context.object.location.z)

    cubeList.append(duplicate(tempCube))
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y - cubeSize, bpy.context.object.location.z)

    cubeList.append(duplicate(tempCube))
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y, bpy.context.object.location.z + cubeSize)

    cubeList.append(duplicate(tempCube))
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y, bpy.context.object.location.z - cubeSize)

def createLastIteration(cube):
    # Definition von cube als Objekt stimmt noch nicht, bzw. die Selektion als ausgewähltes Objekt (obj.select_set(True))
    tempCube: bpy.types.Object = cube
    tempCube.select_set(True)
    bpy.context.view_layer.objects.active = tempCube
    cubeSize = bpy.context.object.dimensions[0] * 3/4

    duplicate(tempCube)
    bpy.context.object.location =  (bpy.context.object.location.x + cubeSize, bpy.context.object.location.y, bpy.context.object.location.z)

    duplicate(tempCube)
    bpy.context.object.location =  (bpy.context.object.location.x - cubeSize, bpy.context.object.location.y, bpy.context.object.location.z)

    duplicate(tempCube)
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y + cubeSize, bpy.context.object.location.z)

    duplicate(tempCube)
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y - cubeSize, bpy.context.object.location.z)

    duplicate(tempCube)
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y, bpy.context.object.location.z + cubeSize)

    duplicate(tempCube)
    bpy.context.object.location =  (bpy.context.object.location.x, bpy.context.object.location.y, bpy.context.object.location.z - cubeSize)
    

def iterateCube(iterations, firstIteration):

    if bool(firstIteration) == False:
        if iterations > 1:
            iterations -= 1
            for i in cubeList:
                createIterationRemaining(i)
            iterateCube(iterations, False)
        
        elif iterations == 1:
            iterations -= 1
            for i in cubeList:
                createLastIteration(i)
            # wird aktuell nicht ausgeführt:
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.join()
            dimensions = bpy.context.object.dimensions
            bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            bpy.context.object.location = (0,0,0)
            bpy.ops.object.transform_apply(scale=True)

    elif bool(firstIteration) == True:
        cube = bpy.data.objects['Cube']
        cube.select_set(True)
        bpy.context.view_layer.objects.active = cube

        if iterations > 1:
            iterations -= 1
            createIterationRemaining(cube)
            iterateCube(iterations, False)
        
        elif iterations == 1:
            iterations -= 1
            createLastIteration(cube)
            # wird aktuell nicht ausgeführt:
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.join()
            dimensions = bpy.context.object.dimensions
            bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            bpy.context.object.location = (0,0,0)
            bpy.ops.object.transform_apply(scale=True)



createCube(1)
iterateCube(1, True)
