import os
import shutil
from blocks import generate_page


def copy_directory(directory_path, destination_path):
    """copying everything from one file path to another"""
    contents = os.listdir(directory_path)
    if contents:
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path):
                print(f"Copying {path}...")
                shutil.copy(path, destination_path)
            else:
                new_directory_destination = os.path.join(destination_path, content)
                if not os.path.exists(new_directory_destination):
                    print(f"Copying the directory path {path}...")
                    os.mkdir(new_directory_destination)
                copy_directory(path, new_directory_destination)
            

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    if contents:
        for content in contents:
            path = os.path.join(dir_path_content, content)
            destination_path = os.path.join(dest_dir_path, content)
            if os.path.isfile(path) and path.endswith(".md"):
                generate_page(path, template_path, (destination_path[:-2] + "html"))
            else:
                if os.path.isdir(path):
                    generate_pages_recursive(path, template_path, destination_path)
                



def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()