from multiprocessing import Value
import os
from pathlib import Path
import shutil

from markdown_blocks import markdown_to_html_node


def copy_content(src="static", dist="public"):
    print(f"start copy: from {src} to {dist}")
    if not os.path.exists(src) or os.path.isfile(src):
        raise ValueError(f"invalid path to source directory {src}")
    if os.path.exists(dist):
        if os.path.isdir(dist):
            shutil.rmtree(dist)
        else:
            raise Exception(f"dist path exists and is not a directory: {dist}")
    os.mkdir(dist)
    print("[v] dist folder erased")

    paths = get_paths(src)
    for path in paths:
        dist_path = path.replace(f"{src}/", f"{dist}/", 1)
        os.makedirs(os.path.dirname(dist_path), exist_ok=True)
        print(f"copy from {path} to {dist_path}")
        shutil.copy(path, dist_path)
    print("finish copy")

def get_paths(dir):
    paths = []
    dir_list = os.listdir(dir)
    for item in dir_list:
        path = os.path.join(dir, item)
        if os.path.isfile(path):
            paths.append(path)
        else:
            paths.extend(get_paths(path))
    return paths

def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no title found")

def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(from_path):
        raise ValueError(f"non existent from_path: {from_path}")
    if not os.path.exists(template_path):
        raise ValueError(f"non existent template_path: {template_path}")

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    html_content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)
    full_html = full_html.replace("href=\"/", f"href={basepath}")
    full_html = full_html.replace("src=\"/", f"src={basepath}")
    dirpath = os.path.dirname(dest_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"non existent dir_path_content: {dir_path_content}")
    if not os.path.exists(template_path):
        raise ValueError(f"non existent template_path: {template_path}")
    if os.path.isfile(dest_dir_path):
        raise ValueError(f"dest_dir should be dir but file provided: {dest_dir_path}")
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_filename = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_filename, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
