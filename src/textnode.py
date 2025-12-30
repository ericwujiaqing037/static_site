from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    # QUOTE = "blockquote"
    # UNORDERED_LIST = "unordered_list"
    # ORDERED_LIST = "ordered_list"

# class Delimiter(Enum):
#     BOLD = "**"
#     ITALIC = "_"
#     CODE = "`"

    
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
            return LeafNode(tag = "code", value = text_node.text)
        case TextType.IMAGE:
            return LeafNode(tag = "img", value = "", props={"src":text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Missing TextType")
        
