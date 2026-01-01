from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "#"
    CODE = "```"
    QUOTE = "> "
    UNORDERED_LIST = "- "
    ORDERED_LIST = ". "


# return list of markdown texts that maps to html blocks
def markdown_to_blocks(markdown_text):

    resultant_blocks = []
    splitted_parts = markdown_text.split("\n\n")

    for part in splitted_parts:
        part_stripped = part.strip()
        if not part:
            continue
        resultant_blocks.append(part_stripped)
    
    return resultant_blocks


def block_to_block_type(block):
    
    # check heading
    for i in range(1, 7):
        heading = BlockType.HEADING.value * i + " "
        if block.startswith(heading):
            return BlockType.HEADING

    # check code block
    if len(block) >= 6 and block.startswith(BlockType.CODE.value) and block.endswith(BlockType.CODE.value):
        return BlockType.CODE
    
    quotedBlocks = True
    unorderedList = True
    orderedList = True

    splitted_blocks = block.split("\n")

    # check for quote, unordered list, ordered list
    for index, b in enumerate(splitted_blocks):
        if b and not b.startswith(BlockType.QUOTE.value):
            quotedBlocks = False

        if b and not b.startswith(BlockType.UNORDERED_LIST.value):
            unorderedList = False

        if b and not b.startswith(str(index + 1) + BlockType.ORDERED_LIST.value):
            orderedList = False            

    if quotedBlocks:
        return BlockType.QUOTE
    
    if unorderedList:
        return BlockType.UNORDERED_LIST

    if orderedList:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown_text):
    # converts a md text into html node 

    blocks = markdown_to_blocks(markdown_text)
    children_html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH: # terminal block
                # must be leaf node -> list of list nodes returned
                paragraph_html_node = md_paragraph_block_to_htmlNode(block)
                children_html_nodes.append(paragraph_html_node)
                
            case BlockType.HEADING: # terminal block
                heading_html_node = md_heading_block_to_htmlNode(block)
                children_html_nodes.append(heading_html_node)
                
            case BlockType.CODE: 
                code_html_node = md_coding_block_to_htmlNode(block)
                children_html_nodes.append(code_html_node)
                
            case BlockType.QUOTE:
                quote_html_node = md_quote_block_to_htmlNode(block)
                children_html_nodes.append(quote_html_node)

            case BlockType.ORDERED_LIST:
                ordered_list_html_node = md_ordered_list_block_to_htmlNode(block)
                children_html_nodes.append(ordered_list_html_node)

            case BlockType.UNORDERED_LIST:
                unordered_list_html_node = md_unordered_list_block_to_htmlNode(block)
                children_html_nodes.append(unordered_list_html_node)

    return HTML_N.ParentNode(tag = LN.Tag.BODY, children=children_html_nodes)

def md_paragraph_block_to_htmlNode(block):
    # nested elements?
    child_text_nodes = TN.text_to_textnodes(block)

    pass

def md_heading_block_to_htmlNode(block):
    pass 

def md_coding_block_to_htmlNode(block):
    pass

def md_quote_block_to_htmlNode(block):
    pass

def md_ordered_list_block_to_htmlNode(block):
    pass

def md_unordered_list_block_to_htmlNode(block):
    pass



