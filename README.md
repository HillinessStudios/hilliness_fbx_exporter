

This is a simple tool to export fbx files using blender

files will be copied to:
    WORK_DIR/Assets (i.e. a local cache)
    TARGET_DIR      (e.g. O3DE_PRJ_DIR/Assets)

files starting in player_ or char_ will append
    Characters/CHAR_NAME/   (you need to create these
                             ideal to store the emotionfx
                             files there too
                            )
    to the path

files containing motion will use the 
    update_fbx_motion_export 
script


Install either via pip or copy the files to your blender source folder

call via:
python -m hilliness_fbx_exporter.update_scan_fbx WORK_DIR TARGET_DIR
