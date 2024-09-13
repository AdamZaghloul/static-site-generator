from textnode import *
from conversions import *
import shutil
import os.path

def main():

    #textnode = TextNode("this is some text", "text type", "www.swag.com")
    #print(textnode.__repr__())
    generate_public()

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

main()