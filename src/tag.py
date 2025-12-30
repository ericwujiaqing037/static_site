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

def tagOpeningRendering(tag):
    return f"<{tag}>"

def tagClosingRendering(tag):
    return f"</{tag}>"