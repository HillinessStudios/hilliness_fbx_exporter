import bpy
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
        object_types={
            "ARMATURE",
        },
        filepath=TARGET_FNAME,
        axis_forward=AXIS_FORWARD,
        axis_up=AXIS_UP,
        armature_nodetype=ARMATURE_NODETYPE,
        # apply_scale_options = 'FBX_SCALE_UNITS',
        add_leaf_bones=False,
        use_armature_deform_only=True,
        bake_anim=True,
        bake_anim_use_nla_strips=False,
        bake_anim_use_all_bones=True,
        # bake_anim_use_all_actions=False,
        # bake_anim_force_startend_keying=False
        # primary_bone_axis=AXIS_FORWARD,
        # secondary_bone_axis=AXIS_UP,
    )
)
