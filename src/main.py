import shutil
import sys

from textnode import TextNode
from pathlib import Path
from helper import copy_directory_content, generate_pages_recursive




def main():
        
    base_path = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # parent_folder_path = Path(__file__).resolve()
    parent_folder_path = Path(base_path)
    static_folder_path = parent_folder_path.parent.parent / 'static'
    # public_folder_path = parent_folder_path.parent.parent / 'public'

    docs_folder_path = Path("docs")

    # if public_folder_path.exists() and public_folder_path.is_dir():
    #     shutil.rmtree(public_folder_path)

    # public_folder_path.mkdir()

    copy_directory_content(src_path=static_folder_path, dst_path= docs_folder_path)
    
    generate_pages_recursive(dir_path_content=Path("content"), template_path=Path("template.html"), dest_dir_path = docs_folder_path)
if __name__ == "__main__":
    main()
