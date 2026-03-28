from textnode import TextNode, TextType
from extractmarkdown import generate_page
import os
import shutil


def copyContent(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    if not os.path.exists(source):
        raise FileNotFoundError
    files = os.listdir(source)
    for file in files:
        src_path = os.path.join(source, file)
        dst_path = os.path.join(dest, file)
        if os.path.isfile(src_path):
            print(f"copying file: {src_path}, to {dst_path}")
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            copyContent(src_path, dst_path)

def generate_pages_recursive(src, template, dest):
    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dest, file)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template, dst_path)
        elif file.endswith(".md"):
            dst_path = dst_path[:-3] + ".html"
            generate_page(src_path, template, dst_path)


def main():
    copyContent("static", "public")
    generate_pages_recursive("content", "template.html", "public")



if __name__ == "__main__":
    main()