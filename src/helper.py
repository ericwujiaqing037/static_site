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
    '''
    
    Args:
        from_path: md file to be converted
        template_path: template file to be filled with the converted html from md file at from_path
        # dest_path: final index.html to be displayed -> eg content(dest_path) = template(converted(content of from_path))
    
    '''

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_txt = from_path.read_text(encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")

    md_title = extract_title(markdown_txt)
    converted_html = markdown_to_html_node(markdown_txt).to_html()

    updated_template = template.replace("{{ Title }}", md_title).replace("{{ Content }}", converted_html)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    dest_path.write_text(updated_template, encoding="utf-8")



'''
Create a generate_pages_recursive(dir_path_content, template_path, dest_dir_path) function. It should:
Crawl every entry in the content directory 
For each markdown file found, generate a new .html file using the same template.html. The generated pages should be written to the public directory in the same directory structure.
Change your main function to use generate_pages_recursive instead of generate_page. You should generate a page for every markdown file in the content directory and write the results to the public directory.

'''


'''
context -> don't want to 


'''

def generate_pages_recursive(dir_path_content:Path, template_path: Path, dest_dir_path: Path):
    #steps: 
        #1 list the contents in the dir_path_content:
        #2 for each file in the dir_path content:
            # if file is markdown -> call generate page
            # elif file is a directory -> update dir_path_content + dest_dir_path -> recursive call

    for child in dir_path_content.iterdir():
        if child.is_dir():
            # update dir_path, and dest_dir_path, keep template path the same
            child_dest_dir_path = dest_dir_path / child.name
            generate_pages_recursive(dir_path_content=child, template_path= template_path, dest_dir_path= child_dest_dir_path)
        if child.suffix == '.md':
            #check the need for path update
            child_dest_dir_path = dest_dir_path / child.with_suffix(".html").name
            generate_page(from_path = child, template_path = template_path, dest_path = child_dest_dir_path)


    
