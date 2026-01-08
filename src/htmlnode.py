from enum import Enum
import html

class Tag(Enum):
    HTML = "html"
    HEAD = "head"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    P = "p"
    HYPERLINK = "a"
    BOLD = "b"
    ITALIC = "i"
    SPAN = "span"
    DIV = "div"
    IMG = "img"
    CODE = "code"
    QUOTE = "blockquote"
    ORDERED_LIST = "ol"
    UNORDERED_LIST = "ul"
    LIST_ITEM = "li"
    PREFORMATTED = "pre"

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag.value}, {self.value}, children: {self.children}, {self.props})"


class ParentNode(HTMLNode):
    '''
    Represents a 'Branch' in the HTML tree. 
    It contains a list of 'children' nodes but holds no raw text itself.
    Used for structural tags like <div>, <p>, <ul>, etc.
    '''    

    def __init__(self, tag, children, value = None , props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag value")
        
        res = ""
        
        for child in self.children:
            if not child.value and child.children is None and child.props is None:
                raise ValueError("Child missing value" + " " + child.tag.value)
            if child is None:
                raise ValueError("Child is none")
            res += child.to_html()
        
        return f"<{self.tag.value}>" + res + f"</{self.tag.value}>"

    
class LeafNode(HTMLNode):
    '''
    Represents a 'Leaf' (endpoint) in the HTML tree.
    It holds raw data (text value or image props) and cannot have children.
    '''

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children= None, props = props)

    def to_html(self):
        if self.value is None and self.tag != Tag.IMG and self.tag != Tag.HYPERLINK:
            raise ValueError("Value is None: All leaf nodes must have value")
        
        safe_props = self.props or {}
        # safe_value = html.escape(self.value, quote=True)
        safe_value = self.value
        match self.tag: 
            case None:
                return safe_value

            case Tag.HYPERLINK:
                safe_props = self.props or {}
                return (f"<a href=\"{safe_props["href"]}\">" 
                        + f"{safe_value}"
                        + f"</a>"
                )
            case Tag.IMG:
                return (f"<{Tag.IMG.value} src =\"{safe_props.get('src', "")}\" alt=\"{safe_props.get('alt', "")}\" />")
            
            case _:
                return ( f"<{self.tag.value}>"
                        + f"{safe_value}"
                        + f"</{self.tag.value}>"
                )