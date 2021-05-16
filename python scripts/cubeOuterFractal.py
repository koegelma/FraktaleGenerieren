import bpy

cubeList = []

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def createCube(cSize): 

    bpy.ops.mesh.primitive_cube_add(size=cSize, location=(0, 0, 0), scale=(1, 1, 1))


def duplicate(cube, iterationRemaining):

    bpy.ops.object.select_all(action='DESELECT')
    cube.select_set(True)
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False})
    if bool(iterationRemaining) == True:
        duplicatedCube = bpy.context.selected_objects[0]
        cubeList.append(duplicatedCube)
    dimensions = bpy.context.object.dimensions
    bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2


def createIterationRemaining(cube):

    bpy.ops.object.select_all(action='DESELECT')
    cube.select_set(True)
    bpy.context.view_layer.objects.active = cube
    cubeSize = bpy.context.object.dimensions[0] * 3/4

    x = bpy.context.object.location.x
    y = bpy.context.object.location.y
    z = bpy.context.object.location.z

    duplicate(cube, True)
    bpy.context.object.location =  (x + cubeSize, y, z)

    duplicate(cube, True)
    bpy.context.object.location =  (x - cubeSize, y, z)

    duplicate(cube, True)
    bpy.context.object.location =  (x, y + cubeSize, z)

    duplicate(cube, True)
    bpy.context.object.location =  (x, y - cubeSize, z)

    duplicate(cube, True)
    bpy.context.object.location =  (x, y, z + cubeSize)

    duplicate(cube, True)
    bpy.context.object.location =  (x, y, z - cubeSize)

def createLastIteration(cube):
    
    bpy.ops.object.select_all(action='DESELECT')
    cube.select_set(True)
    bpy.context.view_layer.objects.active = cube
    cubeSize = bpy.context.object.dimensions[0] * 3/4

    x = bpy.context.object.location.x
    y = bpy.context.object.location.y
    z = bpy.context.object.location.z

    duplicate(cube, False)
    bpy.context.object.location =  (x + cubeSize, y, z)

    duplicate(cube, False)
    bpy.context.object.location =  (x - cubeSize, y, z)

    duplicate(cube, False)
    bpy.context.object.location =  (x, y + cubeSize, z)

    duplicate(cube, False)
    bpy.context.object.location =  (x, y - cubeSize, z)

    duplicate(cube, False)
    bpy.context.object.location =  (x, y, z + cubeSize)

    duplicate(cube, False)
    bpy.context.object.location =  (x, y, z - cubeSize)
    

def iterateCube(iterations, firstIteration):

    if iterations == 0:
        return

    if bool(firstIteration) == False:
        if iterations > 1:
            iterations -= 1
            for i in cubeList:
                createIterationRemaining(i)
                cubeList.remove(i)
            #iterateCube(iterations, False)
        
        elif iterations == 1:
            iterations -= 1
            for i in cubeList:
                createLastIteration(i)
                cubeList.remove(i)
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.join()
            dimensions = bpy.context.object.dimensions
            bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            bpy.context.object.location = (0,0,0)
            bpy.ops.object.transform_apply(scale=True)
            return

    elif bool(firstIteration) == True:
        cube = bpy.data.objects['Cube']
        cube.select_set(True)
        bpy.context.view_layer.objects.active = cube

        if iterations > 1:
            iterations -= 1
            createIterationRemaining(cube)
            #iterateCube(iterations, False)
        
        elif iterations == 1:
            iterations -= 1
            createLastIteration(cube)
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.join()
            dimensions = bpy.context.object.dimensions
            bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            bpy.context.object.location = (0,0,0)
            bpy.ops.object.transform_apply(scale=True)
            return
    
    iterateCube(iterations, False)



createCube(1)
iterateCube(2, True)
