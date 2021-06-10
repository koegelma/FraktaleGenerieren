import bpy
import math

region, rv3d, v3d, area = view3d_find(True)

override = {
    'scene'  : bpy.context.scene,
    'region' : region,
    'area'   : area,
    'space'  : v3d
}

def deleteAll():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete() 

def createCube(cSize): 

    bpy.ops.mesh.primitive_cube_add(size=cSize, location=(0, 0, 0), scale=(1, 1, 1))


def createSphere(cRadius):

    bpy.ops.mesh.primitive_uv_sphere_add(radius=cRadius, location=(0, 0, 0), scale=(1, 1, 1))

def sinCosSphere(frequency, amplitude):
    #frequency = 10
    #amplitude = 0.2

    currentmesh = bpy.context.object.data

    for vert in currentmesh.vertices:
        vert.co.y += amplitude * math.sin(frequency * vert.co.z)
        vert.co.x += amplitude * math.cos(frequency * vert.co.z)

    currentmesh.update()

def view3d_find( return_area = False ):
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    if return_area: return region, rv3d, v3d, area
                    return region, rv3d, v3d
    return None, None

def loopcut():

    bpy.ops.mesh.loopcut_slide(
        override, 
        MESH_OT_loopcut = {
            "number_cuts"           : 10,
            "smoothness"            : 0,     
            "falloff"               : 'SMOOTH',  # Was 'INVERSE_SQUARE' that does not exist
            "edge_index"            : 9,
            "mesh_select_mode_init" : (True, False, False)
        },
        TRANSFORM_OT_edge_slide = {
            "value"           : 0,
            "mirror"          : False, 
            "snap"            : False,
            "snap_target"     : 'CLOSEST',
            "snap_point"      : (0, 0, 0),
            "snap_align"      : False,
            "snap_normal"     : (0, 0, 0),
            "correct_uv"      : False,
            "release_confirm" : False
        }
    )

def sinCosCube():

    #bpy.ops.object.editmode_toggle()
    
    #bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":10, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":9, "mesh_select_mode_init":(True, False, False)}, TRANSFORM_OT_edge_slide={"value":0, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False})

    #bpy.ops.object.editmode_toggle()

    loopcut()

    currentmesh = bpy.context.object.data

    for vert in currentmesh.vertices:
    
        angle = math.radians((vert.co.z + 1) * 45)
    
        x = vert.co.x * math.cos(angle) - vert.co.y * math.sin(angle)
        y = vert.co.x * math.sin(angle) + vert.co.y * math.cos(angle)

        vert.co.x = x
        vert.co.y = y

    currentmesh.update()


deleteAll()
createCube(1)
#createSphere(1)
#sinCosSphere(10,0.2)
sinCosCube()