from pathlib import Path
from blocks import markdown_to_html_node
import shutil


def extract_title(markdown:str):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith("# "):
            result = line.strip("# ").strip()
            print(result)
            return result
            
    raise Exception("No H1 header found")

def copy_directory_content(src_path: Path, dst_path: Path):
    if not src_path or not src_path.exists():
        return False
    
    shutil.copytree(src= src_path, dst = dst_path, dirs_exist_ok=True)
    return True
    

def generate_page(from_path:Path , template_path:Path, dest_path:Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_txt = from_path.read_text(encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")

    md_title = extract_title(markdown_txt)
    converted_html = markdown_to_html_node(markdown_txt).to_html()

    updated_template = template.replace("{{ Title }}", md_title).replace("{{ Content }}", converted_html)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    dest_path.write_text(updated_template, encoding="utf-8")