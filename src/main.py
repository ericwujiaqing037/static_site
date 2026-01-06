from textnode import TextNode
from pathlib import Path
from helper import copy_directory_content, generate_page





def main():

    parent_folder_path = Path(__file__).resolve()
    static_folder_path = parent_folder_path.parent.parent / 'static'
    public_folder_path = parent_folder_path.parent.parent / 'public'

    copy_directory_content(src_path=static_folder_path, dst_path= public_folder_path)

    
    generate_page(from_path=Path("content/index.md"), template_path=Path("template.html"), dest_path=Path("public/index.html"))
    
if __name__ == "__main__":
    main()
