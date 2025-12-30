from htmlnode import HTMLNode
from leafnode import LeafNode
from tag import Tag, tagOpeningRendering, tagClosingRendering


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
        
        return tagOpeningRendering(self.tag) + res + tagClosingRendering(self.tag)
    

def main():
    node = ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )

    
    print(node.to_html())

if __name__ == "__main__":
    main()

