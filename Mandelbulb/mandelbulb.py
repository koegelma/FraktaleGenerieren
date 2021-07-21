import bpy
import math
import mathutils
from mathutils import Color, Vector
import random

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)


class NODE_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "Custom Node Group"
    bl_idname = "OBJECT_PT_MAINPANEL"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = "New Tab"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('node.iteration_operator')

def create_iterations(context, operator, group_name):
    bpy.context.scene.use_nodes = True
    iteration = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    iteration.inputs.new('NodeSocketFloat', 'n')
    iteration.inputs.new('NodeSocketVector', 'zVector')
    iteration.inputs.new('NodeSocketVector', 'c')
    iteration.inputs.new('NodeSocketFloat', 'limit')
    iteration.inputs.new('NodeSocketFloat', 'length')
    iteration.inputs.new('NodeSocketInt', 'iteration')

    iteration.outputs.new('NodeSocketFloat', 'n')
    iteration.outputs.new('NodeSocketVector', 'zVector')
    iteration.outputs.new('NodeSocketVector', 'c')
    iteration.outputs.new('NodeSocketFloat', 'limit')
    iteration.outputs.new('NodeSocketFloat', 'length')
    iteration.outputs.new('NodeSocketInt', 'iteration')


    iteration.outputs[0].default_value = iterate(iteration.inputs[0], iteration.inputs[1], iteration.inputs[2], iteration.inputs[3], iteration.inputs[4], iteration.inputs[5])[0]
    iteration.outputs[1].default_value = iterate(iteration.inputs[0], iteration.inputs[1], iteration.inputs[2], iteration.inputs[3], iteration.inputs[4], iteration.inputs[5])[1]
    iteration.outputs[2].default_value = iterate(iteration.inputs[0], iteration.inputs[1], iteration.inputs[2], iteration.inputs[3], iteration.inputs[4], iteration.inputs[5])[2]
    iteration.outputs[3].default_value = iterate(iteration.inputs[0], iteration.inputs[1], iteration.inputs[2], iteration.inputs[3], iteration.inputs[4], iteration.inputs[5])[3]
    iteration.outputs[4].default_value = iterate(iteration.inputs[0], iteration.inputs[1], iteration.inputs[2], iteration.inputs[3], iteration.inputs[4], iteration.inputs[5])[4]
    iteration.outputs[5].default_value = iterate(iteration.inputs[0], iteration.inputs[1], iteration.inputs[2], iteration.inputs[3], iteration.inputs[4], iteration.inputs[5])[5]
    
    return iteration




class NODE_OT_ITERATION(bpy.types.Operator):
    bl_label = "Add Iteration Node"
    bl_idname = "node.iteration_operator"

    def execute(self, context):
        custom_node_name = "Iteration Node"
        my_group = create_iterations(self, context, custom_node_name)
        test_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        test_node.node_tree = bpy.data.node_groups[my_group.name]
        test_node.use_custom_color = True
        test_node.color = (0.5, 0.4, 0.3)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(NODE_PT_MAINPANEL)
    bpy.utils.register_class(NODE_OT_ITERATION)

def unregister():
    bpy.utils.unregister_class(NODE_PT_MAINPANEL)
    bpy.utils.unregister_class(NODE_OT_ITERATION)

if __name__ == "__main__":
    register()


def iterate(n: float, zVector: Vector, c: Vector, limit: float, length: float, iteration: int):
    newZVector = c + rhoThetaPhiXYZ(n, zVector)
    newLength = vectorLength(newZVector)
    if(length<limit):
        newIteration = iteration + 1
    else:
        newIteration = 0
    return (n, newZVector, c, limit, newLength, newIteration)
def vectorLength(vector):
    return math.sqrt(math.pow(vector[1])+math.pow(vector[2])+math.pow(vector[3]))
def rhoThetaPhiXYZ(n, zVector):
    rho: float = calculateRho(zVector)
    theta = calculateTheta(zVector)
    phi = calculatePhi(zVector)
    x = calculateX(theta, phi, n)
    y = calculateY(theta, phi, n)
    z = calculateZ(theta, n)
    power = math.pow(rho, n)
    outputVector = (power*x,power*y,power*z)
    return outputVector
def calculateRho(inputVector):
    rho: float = math.sqrt(math.pow(inputVector[1], 2) + math.pow(inputVector[2], 2) + math.pow(inputVector[3], 2))
    return rho
def calculateTheta(inputVector):
    theta = math.atan2(inputVector[3] / (math.sqrt(math.pow(inputVector[1], 2) + math.pow(inputVector[2], 2))))
    return theta
def calculatePhi(inputVector):
    phi = math.atan2(inputVector[1] / inputVector[2])
    return phi
def calculateX(theta, phi, n):
    x = math.sin(n*theta)*math.cos(n*phi)
    return x
def calculateY(theta, phi, n):
    y = math.sin(n*theta)*math.sin(n*phi)
    return y
def calculateZ(theta, n):
    z = math.cos(n*theta)
    return z

