from enum import Enum

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
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, value = None , props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag value")
        
        res = ""
        
        for child in self.children:
            if not child.value and child.children is None:
                raise ValueError("Child missing value" + " " + child.tag)
            
            res += child.to_html()
        
        return f"<{self.tag}>" + res + f"</{self.tag}>"

    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children= None, props = props)

    def to_html(self):
        if self.value is None and self.tag != Tag.IMG and self.tag != Tag.HYPERLINK:
            raise ValueError("Value is None: All leaf nodes must have value")
        
        match self.tag: 
            case None:
                return self.value

            case Tag.HYPERLINK:
                safe_props = self.props or {}
                return (f"<a href=\"{safe_props["href"]}\">" 
                        + f"{self.value}"
                        + f"</a>"
                )
            case Tag.IMG:
                return (f"<{Tag.IMG.value} src =\"{safe_props.get('src', "")}\" alt=\"{safe_props.get('alt', "")}\" />")
            
            case _:
                return ( f"<{self.tag.value}>"
                        + f"{self.value}"
                        + f"</{self.tag.value}>"
                )