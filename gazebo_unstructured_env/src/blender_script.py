##code to copy-paste into the text editor in blender (works in blender 2.79) 

import bpy
import numpy as np
import pandas as pd
import os

df = pd.read_csv("YOUR_CSV"))
print("loaded")

#In case we finally do not want thin cylinders and cubes but just large ones
replace_thin_by_large = False

#create the plane:
bpy.ops.mesh.primitive_plane_add(radius=1, location=(0,0,0))
ob = bpy.context.selected_objects[0]
bpy.context.scene.objects.active = ob
bpy.context.object.scale = [32,32,1]#original size is 2x2

tree_dict = {
    "tree_00": "tree_no_leaf_2.stl",
    "tree_01": "tree_no_leaf_3.stl",
    "tree_02": "tree_no_leaf_4.stl",
    "tree_03": "tree_no_leaf_6.stl",
    "tree_04": "tree_no_leaf_7.stl",
    "tree_05": "tree_no_leaf_8.stl",
    "tree_06": "tree_no_leaf_11.stl",
    "tree_07": "tree_no_leaf_12.stl",
    "tree_08": "tree_no_leaf_13.stl",
    "tree_09": "tree_no_leaf_thick_1.stl",
    "tree_10": "tree_no_leaf_thick_2.stl",
    "tree_11": "tree_no_leaf_thick_3.stl",
    "tree_12": "tree_no_leaf_thick_4.stl",
    "tree_13": "tree_no_leaf_thick_5.stl",
    "tree_14": "tree_no_leaf_thick_6.stl"
}


for i in range(df.shape[0]-1):
    info = df.loc[i]
    if (info.at["elem"] == "rect") or (info.at["elem"] == "rect_thin") :
        bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
    elif (info.at["elem"] == "cyl") or (info.at["elem"] == "cyl_thin") :
        bpy.ops.mesh.primitive_cylinder_add(location=(0,0,0))
    else:
        treename = tree_dict[info.at["elem"]]
        bpy.ops.import_mesh.stl(filepath=os.path.join(base_dir,"trees_models",treename))
        bpy.context.object.rotation_euler[0] = 0
        ob = bpy.context.selected_objects[0]
        bpy.context.scene.objects.active = ob
        bpy.context.object.scale = [info.at["hscale"],info.at["hscale"],info.at["vscale"]]
        bpy.context.object.location = [info.at["x"],info.at["y"],info.at["z"]]
        bpy.context.object.rotation_euler[2] = info.at["yaw"]
        bpy.context.object.rotation_euler[0] = 1.5707963267948966
        continue
    ob = bpy.context.selected_objects[0]
    bpy.context.scene.objects.active = ob
    #just to put only large rect and cyl
    if (replace_thin_by_large) and ((info.at["elem"] == "rect") or (info.at["elem"] == "rect_thin")) :
        bpy.context.object.scale = [info.at["hscale"]+1,info.at["hscale"]+1,info.at["vscale"]]
    else:
        bpy.context.object.scale = [info.at["hscale"],info.at["hscale"],info.at["vscale"]]
    bpy.context.object.location = [info.at["x"],info.at["y"],info.at["z"]+1.0]
    bpy.context.object.rotation_euler[2] = info.at["yaw"]
