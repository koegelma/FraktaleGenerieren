import bpy
import math
import random
from bpy.types import Operator
from bpy.props import IntProperty

bl_info = {
    "name": "Fractal Generator",
    "author": "Johann / Marius",
    "description": "Generate/Modify Fractal Objects",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}


class OBJECT_OT_iterations_outer(bpy.types.Operator):
    """ Add iterations for an object """
    bl_idname = "object.add_iterations_outer"
    bl_label = "Add Iterations"
    bl_options = {"REGISTER", "UNDO"}

    ITERATIONS: bpy.props.IntProperty(
        name="Number of Iterations",
        description="WARNING: Creating more than 3 Iterations could lead to performance issues!",
        default=1
        # options={"HIDDEN"}
    )

    objectList = []
    addToObjectList = []
    alreadyIteratedList = []

    firstIteration = True

    def deleteLists(self):
        self.objectList.clear()
        self.addToObjectList.clear()
        self.alreadyIteratedList.clear()

    def createCube(self, cSize):

        bpy.ops.mesh.primitive_cube_add(
            size=cSize, location=(0, 0, 0), scale=(1, 1, 1))

    def createSphere(self, cRadius):

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=cRadius, location=(0, 0, 0), scale=(1, 1, 1))

    def duplicate(self, object, iterationRemaining):

        bpy.ops.object.select_all(action='DESELECT')
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False})
        if bool(iterationRemaining) == True:
            duplicatedObject = bpy.context.selected_objects[0]
            self.addToObjectList.append(duplicatedObject)
        dimensions = bpy.context.object.dimensions
        bpy.context.object.dimensions = dimensions[0] / \
            2, dimensions[1] / 2, dimensions[2] / 2

    def createIteration(self, object, iterationRemaining):

        bpy.ops.object.select_all(action='DESELECT')
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        objectSize = bpy.context.object.dimensions[0] * 3/4

        x = bpy.context.object.location.x
        y = bpy.context.object.location.y
        z = bpy.context.object.location.z

        self.duplicate(object, iterationRemaining)
        bpy.context.object.location = (x + objectSize, y, z)

        self.duplicate(object, iterationRemaining)
        bpy.context.object.location = (x - objectSize, y, z)

        self.duplicate(object, iterationRemaining)
        bpy.context.object.location = (x, y + objectSize, z)

        self.duplicate(object, iterationRemaining)
        bpy.context.object.location = (x, y - objectSize, z)

        self.duplicate(object, iterationRemaining)
        bpy.context.object.location = (x, y, z + objectSize)

        self.duplicate(object, iterationRemaining)
        bpy.context.object.location = (x, y, z - objectSize)

    def joinAndResize(self):

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.join()
        dimensions = bpy.context.object.dimensions
        bpy.context.object.dimensions = dimensions[0] / \
            2, dimensions[1] / 2, dimensions[2] / 2
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        bpy.context.object.location = (0, 0, 0)
        bpy.ops.object.transform_apply(scale=True)

    def iterateObject(self):
        if self.ITERATIONS == 0:
            return

        if not bool(self.firstIteration):
            if self.ITERATIONS > 1:
                for i in self.objectList:
                    if i not in self.alreadyIteratedList:
                        self.createIteration(i, True)
                        self.alreadyIteratedList.append(i)

            elif self.ITERATIONS == 1:
                for i in self.objectList:
                    if i not in self.alreadyIteratedList:
                        self.createIteration(i, False)
                        self.alreadyIteratedList.append(i)
                self.joinAndResize()

        elif bool(self.firstIteration):
            object = bpy.context.view_layer.objects.active
            object.select_set(True)

            if self.ITERATIONS > 1:
                self.createIteration(object, True)

            elif self.ITERATIONS == 1:
                self.createIteration(object, False)
                self.joinAndResize()

        for i in self.addToObjectList:
            if i not in self.objectList:
                self.objectList.append(i)

        self.ITERATIONS -= 1

        if (self.firstIteration == False):
            self.iterateObject()

        self.firstIteration = False
        self.iterateObject()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        self.iterateObject()

        return {'FINISHED'}


class OBJECT_OT_iterations_inner(bpy.types.Operator):
    """ Add inner iterations for an object """
    bl_idname = "object.add_iterations_inner"
    bl_label = "Add Iterations"
    bl_options = {"REGISTER", "UNDO"}

    ITERATIONS: bpy.props.IntProperty(
        name="Number of Iterations",
        description="WARNING: Creating more than 3 Iterations could lead to performance issues!",
        # min=1,
        # max=5
        default=1
    )

    def iterateObject(self):

        for iteration in range(self.ITERATIONS):
            objectSize = bpy.context.object.dimensions[0]

            for i1 in range(3):

                if i1 != 1:

                    for i in range(2):
                        bpy.ops.object.duplicate()
                        bpy.context.object.location = (
                            bpy.context.object.location.x + objectSize, bpy.context.object.location.y, i1 * objectSize)

                    for i in range(2):
                        bpy.ops.object.duplicate()
                        bpy.context.object.location = (
                            bpy.context.object.location.x, bpy.context.object.location.y + objectSize, i1 * objectSize)

                    for i in range(2):
                        bpy.ops.object.duplicate()
                        bpy.context.object.location = (
                            bpy.context.object.location.x - objectSize, bpy.context.object.location.y, i1 * objectSize)

                    for i in range(2):
                        bpy.ops.object.duplicate()
                        bpy.context.object.location = (
                            bpy.context.object.location.x, bpy.context.object.location.y - objectSize, i1 * objectSize)

            bpy.ops.object.duplicate()
            bpy.context.object.location = (
                bpy.context.object.location.x, bpy.context.object.location.y, bpy.context.object.location.z - objectSize)

            bpy.ops.object.duplicate()
            bpy.context.object.location = (
                bpy.context.object.location.x + objectSize*2, bpy.context.object.location.y, bpy.context.object.location.z)

            bpy.ops.object.duplicate()
            bpy.context.object.location = (
                bpy.context.object.location.x, bpy.context.object.location.y + objectSize*2, bpy.context.object.location.z)

            bpy.ops.object.duplicate()
            bpy.context.object.location = (
                bpy.context.object.location.x - objectSize*2, bpy.context.object.location.y, bpy.context.object.location.z)

            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.join()
            for i in range(self.ITERATIONS):
                dimensions = bpy.context.object.dimensions
                bpy.context.object.dimensions = dimensions[0] / \
                    3, dimensions[1] / 3, dimensions[2] / 3
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            bpy.context.object.location = (0, 0, 0)
            bpy.ops.object.transform_apply(scale=True)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        self.iterateObject()
        return {'FINISHED'}


class OBJECT_OT_spirale(bpy.types.Operator):
    """ Create Fibonacci Spiral """
    bl_idname = "object.create_spirale"
    bl_label = "Create Fibonacci Spiral"
    bl_options = {"REGISTER", "UNDO"}

    OBJECTS: bpy.props.IntProperty(
        name="Number of Objects",
        min=1,
        default=500
    )

    SCALE: bpy.props.FloatProperty(
        name="Scale",
        default=1.3
    )

    objectList = []

    def get_object(self):
        object = bpy.context.view_layer.objects.active
        object.select_set(True)
        return object

    def createSpirale(self):
        object = self.get_object()

        for i in range(self.OBJECTS):

            theta = i * math.radians(137.5)
            r = self.SCALE * math.sqrt(i)
            bpy.ops.object.duplicate_move(
                OBJECT_OT_duplicate={"linked": False})
            bpy.context.object.location = (
                (math.cos(theta) * r, math.sin(theta) * r, 0.0))
            duplicatedObject = bpy.context.selected_objects[0]
            self.objectList.append(duplicatedObject)

        for i in self.objectList:
            i.parent = object
        self.objectList.clear()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        self.createSpirale()
        return {'FINISHED'}


class OBJECT_OT_randomOP(bpy.types.Operator):
    """ Random Operator """
    bl_idname = "object.random_op"
    bl_label = "Feel Lucky?"
    bl_options = {"REGISTER", "UNDO"}

    def joinAndResize(self):

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        bpy.context.object.location = (0, 0, 0)
        bpy.ops.object.transform_apply(scale=True)

    def randomOP(self):

        randomObject = random.randint(1, 6)
        if (randomObject == 1):
            bpy.ops.mesh.primitive_cube_add(
                size=1, location=(0, 0, 0), scale=(1, 1, 1))

        if (randomObject == 2):
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=1, location=(0, 0, 0), scale=(1, 1, 1))

        if (randomObject == 3):
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=1, location=(0, 0, 0), scale=(1, 1, 1))

        if (randomObject == 4):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1, depth=2, location=(0, 0, 0), scale=(1, 1, 1))

        if (randomObject == 5):
            bpy.ops.mesh.primitive_cone_add(
                radius1=1, radius2=0, depth=2, location=(0, 0, 0), scale=(1, 1, 1))

        if (randomObject == 6):
            bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), rotation=(
                0, 0, 0), major_radius=1, minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75)

        max = 3

        for i in range(4):
            randomOperator = random.randint(1, max)
            if (randomOperator == 1):
                bpy.ops.object.add_iterations_outer()
            if (randomOperator == 2):
                bpy.ops.object.add_iterations_inner()
            if (randomOperator == 3):
                bpy.ops.object.create_spirale()
                self.joinAndResize()
                max = 2
                

    def execute(self, context):
        self.randomOP()
        return {'FINISHED'}


class fractalPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Fractal Panel"
    bl_idname = "VIEW_3D_PT_fractalPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Fractal"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Add Objects To Scene: ")
        row = layout.row()
        row.operator("mesh.primitive_cube_add")
        row.operator("mesh.primitive_uv_sphere_add")
        row = layout.row()
        row.operator("mesh.primitive_ico_sphere_add")
        row.operator("mesh.primitive_cylinder_add")
        row = layout.row()
        row.operator("mesh.primitive_cone_add")
        row.operator("mesh.primitive_torus_add")

        layout.label(text="Iterations For Active Object: ")
        row = layout.row()
        row.operator("object.add_iterations_outer", text="Create Iterations")

        row = layout.row()
        row.operator("object.add_iterations_inner",
                     text="Create Inner Iterations")

        layout.label(text="Fibonacci Spiral For Active Object: ")
        row = layout.row()
        row.operator("object.create_spirale", text="Create Fibonacci Spiral")

        layout.label(text="Random:")
        row = layout.row()
        row.operator("object.random_op", text="Will It Crash?")


def register():
    bpy.utils.register_class(OBJECT_OT_iterations_outer)
    bpy.utils.register_class(OBJECT_OT_iterations_inner)
    bpy.utils.register_class(fractalPanel)
    bpy.utils.register_class(OBJECT_OT_spirale)
    bpy.utils.register_class(OBJECT_OT_randomOP)
    bpy.ops.object.add_iterations_outer('INVOKE_DEFAULT')
    bpy.ops.object.add_iterations_inner('INVOKE_DEFAULT')
    bpy.ops.object.create_spirale('INVOKE_DEFAULT')


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_iterations_outer)
    bpy.utils.unregister_class(fractalPanel)
    bpy.utils.unregister_class(OBJECT_OT_iterations_inner)
    bpy.utils.unregister_class(OBJECT_OT_spirale)
    bpy.utils.unregister_class(OBJECT_OT_randomOP)
