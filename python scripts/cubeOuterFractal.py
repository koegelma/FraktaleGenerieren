import bpy

objectList = []
addToObjectList = []
alreadyIteratedList = []



def deleteAll():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete() 

def createCube(cSize): 

    bpy.ops.mesh.primitive_cube_add(size=cSize, location=(0, 0, 0), scale=(1, 1, 1))


def createSphere(cRadius):

    bpy.ops.mesh.primitive_uv_sphere_add(radius=cRadius, location=(0, 0, 0), scale=(1, 1, 1))


def duplicate(object, iterationRemaining):

    bpy.ops.object.select_all(action='DESELECT')
    object.select_set(True)
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False})
    if bool(iterationRemaining) == True:
        duplicatedObject = bpy.context.selected_objects[0]
        addToObjectList.append(duplicatedObject)
    dimensions = bpy.context.object.dimensions
    bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2


def createIteration(object, iterationRemaining):

    bpy.ops.object.select_all(action='DESELECT')
    object.select_set(True)
    bpy.context.view_layer.objects.active = object
    objectSize = bpy.context.object.dimensions[0] * 3/4

    x = bpy.context.object.location.x
    y = bpy.context.object.location.y
    z = bpy.context.object.location.z

    duplicate(object, iterationRemaining)
    bpy.context.object.location =  (x + objectSize, y, z)

    duplicate(object, iterationRemaining)
    bpy.context.object.location =  (x - objectSize, y, z)

    duplicate(object, iterationRemaining)
    bpy.context.object.location =  (x, y + objectSize, z)

    duplicate(object, iterationRemaining)
    bpy.context.object.location =  (x, y - objectSize, z)

    duplicate(object, iterationRemaining)
    bpy.context.object.location =  (x, y, z + objectSize)

    duplicate(object, iterationRemaining)
    bpy.context.object.location =  (x, y, z - objectSize)


def joinAndResize():
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()
    dimensions = bpy.context.object.dimensions
    bpy.context.object.dimensions = dimensions[0] / 2, dimensions[1] / 2, dimensions[2] / 2
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    bpy.context.object.location = (0,0,0)
    bpy.ops.object.transform_apply(scale=True)
    

def iterateObject(iterations, firstIteration):

    if iterations == 0:
        return

    if not bool(firstIteration):
        if iterations > 1:
            for i in objectList:
                if i not in alreadyIteratedList:
                    createIteration(i, True)
                    alreadyIteratedList.append(i)

        elif iterations == 1:
            for i in objectList:
                if i not in alreadyIteratedList:
                    createIteration(i, False)
                    alreadyIteratedList.append(i)
            joinAndResize()
            

    elif bool(firstIteration):
        object = bpy.data.objects['Cube']
        object.select_set(True)
        bpy.context.view_layer.objects.active = object

        if iterations > 1:
            createIteration(object, True)
        
        elif iterations == 1:
            createIteration(object, False)
            joinAndResize()
    
    for i in addToObjectList:
        if i not in objectList:
            objectList.append(i)


    iterations -= 1
    iterateObject(iterations, False)


#deleteAll()
#createCube(1)
#createSphere(1)
#iterateObject(3, True)
