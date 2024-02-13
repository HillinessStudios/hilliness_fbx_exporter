import bpy
import sys
import os

path_join = os.path.join
WORK_DIR = os.getcwd()
TARGET_FNAME = path_join(WORK_DIR, "_export_fbx_")


ARMATURE_NODETYPE = "ROOT"
ARMATURE_NODETYPE = "NULL"
AXIS_FORWARD = "-Z"
AXIS_UP = "Y"


print(
    bpy.ops.export_scene.fbx(
        object_types={"ARMATURE", "MESH", "OTHER"},
        filepath=TARGET_FNAME,
        axis_forward=AXIS_FORWARD,
        axis_up=AXIS_UP,
        armature_nodetype=ARMATURE_NODETYPE,
        use_armature_deform_only=True,
        add_leaf_bones=False,
        # bake_anim=False,
    )
)
