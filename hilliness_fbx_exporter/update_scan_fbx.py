from contextlib import chdir

import glob
import os
import shutil
import subprocess
import sys

path_join = os.path.join
path_dirname = os.path.dirname
path_basename = os.path.basename
getmtime = os.path.getmtime
SEP = os.path.sep


BLENDER_PATH_GUESS = [
    "/Applications/Blender.app/Contents/MacOS/Blender",
    "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe",
    "D:\\opt\\blender\\blender.exe",
]


def adjust_character_path(ctx):
    fname = ctx.fname_blend
    _target_dir = ctx.target_dir
    if fname.startswith("player_") or fname.startswith("char_"):
        character_name = fname.replace(".", "_").split("_")[1]
        character_name = character_name[0].upper() + character_name[1:]
        ctx.target_dir = path_join(_target_dir, "Characters", character_name)


class Context(object):
    def __init__(self, result, target_dir, fname_blend, fname_fbx, fbx_path):
        # subprocess result
        self.result = result
        # target directory
        self.target_dir = target_dir
        # basename for files
        self.fname_blend = fname_blend
        self.fname_fbx = fname_fbx
        # source file
        self.fbx_path = fbx_path


class FBXExporter(object):
    def __init__(self, work_dir):
        self.blender = None
        self.work_dir = work_dir
        self.script_dir = path_dirname(__file__)
        self.post = [
            adjust_character_path,
        ]
        self.verbose = False
        # guess_blender_path
        path_exists = os.path.exists
        for path in BLENDER_PATH_GUESS:
            if path_exists(path):
                print("Found blender: %s" % (path,))
                self.blender = path

    def get_fbx_name(self, fname) -> str:
        fname_src = path_basename(fname)
        # remove the blend bit fromt the filename, append fbx
        return path_join(self.work_dir, "Assets", fname_src[:-5] + "fbx")

    def export_fbx(self, fname_blend, target_dir) -> Context:
        work_dir = self.work_dir
        script = "update_fbx_export.py"
        if "motion" in fname_blend:
            script = "update_fbx_motion_export.py"

        fbx_path = self.get_fbx_name(fname_blend)

        with chdir(work_dir):
            command = [
                self.blender,
                path_join(work_dir, fname_blend),
                "--background",
                "--python",
                path_join(self.script_dir, script),
            ]
            try:
                result = subprocess.check_call(command)
            except TypeError:
                print(command)
                raise
        print(result)
        # remove the cached fbx in workdir/Assets
        try:
            os.remove(fbx_path)
        except FileNotFoundError:
            pass
        # rename the temp file to the cache file filename
        os.rename(path_join(work_dir, "_export_fbx_"), fbx_path)
        fname_fbx = path_basename(fbx_path)
        return Context(
            target_dir=target_dir,
            result=result,
            fname_blend=fname_blend,
            fname_fbx=fname_fbx,
            fbx_path=fbx_path,
        )

    def needs_updating(self, glob_list):
        verbose = self.verbose
        get_fbx_name = self.get_fbx_name
        for fname in glob_list:
            blend_mtime = getmtime(fname)
            try:
                fbx_mtime = getmtime(get_fbx_name(fname))
            except FileNotFoundError:
                fbx_mtime = 0
            fbx_needs_updating = fbx_mtime < blend_mtime
            if fname.startswith("_"):
                continue
            if verbose:
                print(fname, fbx_mtime, blend_mtime, fbx_needs_updating)
            if fbx_needs_updating:
                yield fname

    def run(self, target_dir):
        if self.blender is None:
            raise ValueError("Blender not found")
        export_fbx = self.export_fbx
        needs_updating = self.needs_updating
        pattern = self.work_dir + SEP + "*.blend"
        post_hooks = self.post
        print("pattern: %s" % (pattern,))
        for fname in map(path_basename, needs_updating(glob.glob(pattern))):
            print(fname)
            # export the blend to a temp location
            ctx = export_fbx(fname, target_dir)
            # run post hooks to adjust the file names and directories
            for func in post_hooks:
                func(ctx)
            # build the target path
            _target_path = path_join(ctx.target_dir, ctx.fname_fbx)
            fbx_path = ctx.fbx_path
            # copy it to the target project
            shutil.copyfile(fbx_path, _target_path)
            print("%s -> %s" % (fbx_path, _target_path))


if __name__ == "__main__":
    ARGV = sys.argv[1:]
    FBXExporter(ARGV[0]).run(*ARGV[1:])
