from enum import Enum
from htmlnode import HTMLNode
from tag import Tag


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

            
