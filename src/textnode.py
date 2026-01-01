from enum import Enum
from htmlnode import LeafNode, ParentNode, HTMLNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    QUOTE = "quote"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

DELIMITER_MAP = {
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`" , 
    TextType.QUOTE: ">"
}
   
class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, anotherTextNode):
        return ((self.text == anotherTextNode.text)
            and (self.text_type.value == anotherTextNode.text_type.value)
            and (self.url == anotherTextNode.url)
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag = None, value = text_node.text)
        case TextType.BOLD:
            return LeafNode(tag = "b", value = text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag = "i", value = text_node.text)
        case TextType.CODE:
            return LeafNode(tag = "code", value = text_node.text)
        case TextType.LINK:
            return LeafNode(tag = "link", value = text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag = "img", value = "", props={"src":text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Missing TextType")

def extract_markdown_images_first_occurence(text):
    return re.search(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_regular_links_first_occurence(text):
    return re.search(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_regular_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# splits nodes by its delimiter - only handles BOLD, Italic, Code
def split_nodes_delimiter(old_nodes_list, delimiter, text_type):
    resultant_nodes = []
    for node in old_nodes_list:
        if node.text_type != TextType.TEXT:
            resultant_nodes.append(node)
            continue

        split_results = node.text.split(delimiter, maxsplit = 2)

        if(len(split_results) == 1 or len(split_results) == 2):
            resultant_nodes.append(node)
            continue
        
        prefix = split_results[0]
        enclosed_value = split_results[1]
        postfix = split_results[2]

        if prefix:
            prefixNode = TextNode(prefix, TextType.TEXT)
            resultant_nodes.append(prefixNode)
        
        enclosed_node = TextNode(enclosed_value, text_type)
        resultant_nodes.append(enclosed_node)

        if postfix:
            postfixNode = TextNode(postfix, TextType.TEXT)
            postfix_splitted_node_list = split_nodes_delimiter([postfixNode], delimiter, text_type)
            resultant_nodes.extend(postfix_splitted_node_list)

    return resultant_nodes            

# recursively extract markdown syntax of image: ![Alt Text](URL) into nodes
def split_nodes_image(old_nodes_list):
    # recursively extract markdown syntax of image: ![Alt Text](URL) into nodes
    resultant_nodes = []

    for node in old_nodes_list:
        # if node type is not text, move on
        if node.text_type != TextType.TEXT:
                    resultant_nodes.append(node)
                    continue
        
        first_image_match = extract_markdown_images_first_occurence(node.text)

        if(not first_image_match):
            resultant_nodes.append(node)
            continue

        img_markdown_text = first_image_match.group(0)
        img_alt_text = first_image_match.group(1)
        img_link_address = first_image_match.group(2)
        
        before, after = node.text.split(img_markdown_text, maxsplit = 1)

        if before:
            prefixNode =  TextNode(before, TextType.TEXT)
            resultant_nodes.append(prefixNode)
        
        img_node = TextNode(img_alt_text, TextType.IMAGE, img_link_address)
        resultant_nodes.append(img_node)

        if after:
            postfixNode = TextNode(after, TextType.TEXT)
            postfixNodes_splitted = split_nodes_image([postfixNode])
            resultant_nodes.extend(postfixNodes_splitted)

    return resultant_nodes

  
# recursively extract links from marked down text
def split_nodes_link(old_nodes_list):
    # recursively extract links from marked down text
    resultant_nodes = []
    for node in old_nodes_list:
         
        if node.text_type != TextType.TEXT: # this function only extracts links from text nodes
            resultant_nodes.append(node)
            continue
        
        first_link_match = extract_regular_links_first_occurence(node.text)
    
        if not first_link_match:
            resultant_nodes.append(node)
            continue

        full_link_markdown = first_link_match.group(0)
        hyperlink_text = first_link_match.group(1)
        link_address = first_link_match.group(2)

        before, after = node.text.split(full_link_markdown, maxsplit=1)

        if before:
            prefixNode = TextNode(before, TextType.TEXT)
            resultant_nodes.append(prefixNode)

        cur_link_node = TextNode(hyperlink_text, TextType.LINK, url=link_address)
        resultant_nodes.append(cur_link_node)

        if after:
            postfixNode = TextNode(after, TextType.TEXT)
            extracted_postfix_nodes = split_nodes_link([postfixNode])
            resultant_nodes.extend(extracted_postfix_nodes)
    
    return resultant_nodes

# all in one function that converts raw_markdown text into textnodes (order preserved)
# returns a list of text nodes
def text_to_textnodes(raw_markdown_text):
    parentNode = TextNode(raw_markdown_text, TextType.TEXT)
    returning_nodes = [parentNode]

    for textType in TextType:
        if textType in DELIMITER_MAP:
            returning_nodes = split_nodes_delimiter(returning_nodes, DELIMITER_MAP[textType], textType)

    returning_nodes = split_nodes_image(returning_nodes)
    returning_nodes = split_nodes_link(returning_nodes)

    return returning_nodes
    




