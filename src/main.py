import shutil

from textnode import TextNode
from pathlib import Path
from helper import copy_directory_content, generate_pages_recursive




def main():

    parent_folder_path = Path(__file__).resolve()
    static_folder_path = parent_folder_path.parent.parent / 'static'
    public_folder_path = parent_folder_path.parent.parent / 'public'

    if public_folder_path.exists() and public_folder_path.is_dir():
        shutil.rmtree(public_folder_path)

    public_folder_path.mkdir()

    copy_directory_content(src_path=static_folder_path, dst_path= public_folder_path)
    
    generate_pages_recursive(dir_path_content=Path("content"), template_path=Path("template.html"), dest_dir_path=Path("public"))
if __name__ == "__main__":
    main()
