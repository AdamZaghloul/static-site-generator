from textnode import *
from conversions import *
import shutil
import os.path

def main():

    generate_public()

    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content/", "template.html", "public/")

def generate_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    
    os.mkdir("public")
    
    copy_static("static", "public")

def copy_static(source, destination):
    paths = os.listdir(source)

    for path in paths:
        if os.path.exists(f"{destination}/{path}"):
            pass
        else:
            if os.path.isfile(f"{source}/{path}"):
                shutil.copy(f"{source}/{path}", f"{destination}/")
            else:
                os.mkdir(f"{destination}/{path}")
                copy_static(f"{source}/{path}", f"{destination}/{path}")

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = ""
    template = ""
    
    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()
    
    with open(template_path, encoding="utf-8") as t:
        template = t.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, mode="w", encoding="utf-8") as w:
        w.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    paths = os.listdir(dir_path_content)

    for path in paths:
        if os.path.exists(f"{dest_dir_path}/{path}"):
            pass
        else:
            if os.path.isfile(f"{dir_path_content}/{path}"):
                if path.endswith(".md"):
                    pre, ext = os.path.splitext(f"{path}")
                    generate_page(f"{dir_path_content}/{path}", template_path, f"{dest_dir_path}/{pre}.html")
            else:
                os.mkdir(f"{dest_dir_path}/{path}")
                generate_pages_recursive(f"{dir_path_content}/{path}", template_path, f"{dest_dir_path}/{path}")
main()