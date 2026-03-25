import os, shutil
from markdown_blocks import markdown_to_html_node
from pathlib import Path


def extract_title(markdown):
    lines = markdown.split("\n")
    heading = ""
    for line in lines:
        if line.startswith("# "):
            heading = line[2:]
            break
    if not heading:
        raise ValueError("heading not found")
    return heading

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as f:
        from_markdown = f.read()
    with open(template_path) as f:
        template_contents = f.read()
    html_string = markdown_to_html_node(from_markdown).to_html()
    title = extract_title(from_markdown)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_string)
    template_contents = template_contents.replace('href="/', 'href="{basepath}')
    template_contents = template_contents.replace('src="/', 'src="{basepath}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_contents)

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for path in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, path)
        if os.path.isfile(full_path):
            generate_page(full_path, template_path, Path(os.path.join(dest_dir_path, path)).with_suffix(".html"), basepath)
        else:
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, path), basepath)
