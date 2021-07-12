import bpy
import math

objects = 500
scale = 1.3

objectList = []

def createSpirale():

    object = bpy.context.view_layer.objects.active
    object.select_set(True)

    for i in range(0, objects):

        theta = i * math.radians(137.5)
        r = scale * math.sqrt(i)
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False})
        bpy.context.object.location = (
            (math.cos(theta) * r, math.sin(theta) * r, 0.0))
        duplicatedObject = bpy.context.selected_objects[0]
        objectList.append(duplicatedObject)
    
    for i in objectList:
        i.parent = object


def createCube(cSize):

    bpy.ops.mesh.primitive_cube_add(
        size=cSize, location=(0, 0, 0), scale=(1, 1, 1))


def createSphere(cRadius):

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=cRadius, location=(0, 0, 0), scale=(1, 1, 1))


def createCone():

    bpy.ops.mesh.primitive_cone_add(location=(0, 0, 0), scale=(1, 1, 1))



def deleteAll():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


deleteAll()
#createSphere(1)
#createCube(1)
createCone()
createSpirale()
