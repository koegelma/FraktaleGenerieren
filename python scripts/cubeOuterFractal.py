import bpy



class OBJECT_OT_iterations_outer(bpy.types.Operator):
    """ Add iterations for an object """
    bl_idname = "object.add_iterations_outer"
    bl_label = "Add Iterations"

    objectList = []
    addToObjectList = []
    alreadyIteratedList = []

    firstIteration = True

    iterations: bpy.props.IntProperty(
        name="Iteration count",
        description="How many iterations",
        default=1
    )

    def deleteAll(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

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
        if self.iterations == 0:
            return

        if not bool(self.firstIteration):
            if self.iterations > 1:
                for i in self.objectList:
                    if i not in self.alreadyIteratedList:
                        self.createIteration(i, True)
                        self.alreadyIteratedList.append(i)

            elif self.iterations == 1:
                for i in self.objectList:
                    if i not in self.alreadyIteratedList:
                        self.createIteration(i, False)
                        self.alreadyIteratedList.append(i)
                self.joinAndResize()

        elif bool(self.firstIteration):
            object = bpy.context.view_layer.objects.active
            object.select_set(True)

            if self.iterations > 1:
                self.createIteration(object, True)

            elif self.iterations == 1:
                self.createIteration(object, False)
                self.joinAndResize()

        for i in self.addToObjectList:
            if i not in self.objectList:
                self.objectList.append(i)

        self.iterations -= 1

        if (self.firstIteration == False):
            self.iterateObject()

        self.firstIteration = False
        self.iterateObject()

        

    def execute(self, context):
        self.iterateObject()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_iterations_outer)


def unregister():
    bpy.utils.register_class(OBJECT_OT_iterations_outer)


if __name__ == "__main__":
    register()
    bpy.ops.object.add_iterations_outer()

    # deleteAll()
    # createCube(1)
    # createSphere(1)
    # iterateObject(3, True)
