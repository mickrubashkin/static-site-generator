import os
import shutil


def copy_content(src="static", dist="public"):
    print(f"start copy: from {src} to {dist}")
    # erase public folder
    if not os.path.exists(src) or os.path.isfile(src):
        raise Exception(f"invalid path to source directory {src}")
    if os.path.exists(dist):
        shutil.rmtree(dist)
        os.mkdir(dist)
        print("[v] dist folder erased")

    # cp all the content recursivly from src to dist
    pathes = get_pathes(src, [])
    for path in pathes:
        dist_path = path.replace(f"{src}/", f"{dist}/", 1)
        os.makedirs(os.path.dirname(dist_path), exist_ok=True)
        print(f"copy from {path} to {dist_path}")
        shutil.copy(path, dist_path)
    print("finish copy")

def get_pathes(dir, pathes):
    dir_list = os.listdir(dir)
    for item in dir_list:
        path = os.path.join(dir, item)
        if os.path.isfile(path):
            pathes.append(path)
        else:
            get_pathes(path, pathes)
    return pathes
