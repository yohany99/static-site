import os, shutil

def copy_static(src, dst):
    #delete all contents in dst directory
    if os.path.exists(dst):
        shutil.rmtree(dst)
    #copy all files and subdirectories
    os.mkdir(dst)
    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        dst_path = os.path.join(dst, path)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_static(src_path, dst_path)
        