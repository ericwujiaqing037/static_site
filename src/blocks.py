from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode, Tag
from textnode import TextNode, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "#"
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "- "
    ORDERED_LIST = ". "
    

blockType_to_hmtl_tag = {
    BlockType.PARAGRAPH : Tag.P, 
    BlockType.CODE : Tag.CODE
}

html_headinger_tag_dict = {
    1: Tag.H1, 
    2: Tag.H2,
    3: Tag.H3,
    4: Tag.H4,
    5: Tag.H5,
    6: Tag.H6
}

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
    prefix_hash_tag_counts = 0
    header_delimiter = BlockType.HEADING.value
    trailing_empty_space = False
    for c in block:
        if c == header_delimiter and prefix_hash_tag_counts <= 6 :
            prefix_hash_tag_counts += 1
        else:
            trailing_empty_space = (c == ' ')
            break
    
    if(prefix_hash_tag_counts >= 1 and prefix_hash_tag_counts <= 6 and trailing_empty_space):
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
    '''
    Converts raw markdown text into html node 
    - flat line parser only

    Args:
        raw markdown text  

    Returns:
        HTML node corresponding to the md text
    '''
    
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

    return ParentNode(tag = Tag.DIV, children=children_html_nodes)



def md_terminal_block_to_htmlNode(block:str, htmlTag: Tag):
    """
    Converts block level markdown strings stripped of block tags into corresponding html node
    - flat parsing only
    
    Args: 
        block: string stripped of block tag prefixes and postfixes
        block tag: corresponding tag

    Returns:
        HTML Node created based on input block and block tag.
    """

    textnode_list = text_to_textnodes(block)
    child_html_node_list = []
    
    for tn in textnode_list:
        child_html_node = text_node_to_html_node(tn)
        child_html_node_list.append(child_html_node)

    return ParentNode(htmlTag, child_html_node_list)



def md_paragraph_block_to_htmlNode(block:str):
    '''
    Converts block level md paragraph into html node
    - flat parsing only

    Args:
        block: string of md paragraph
        blog tag: default input of BlockType.PARAGRAPH  
    
    Returns:
        HTML Node created based on input block
    '''

    return md_terminal_block_to_htmlNode(block, htmlTag = Tag.P)
    

def md_heading_block_to_htmlNode(block:str):
    '''
    converts md heading (unstripped of prefixs) into corresponding html node
    - flat parsing only
    
    Args:
        block: md heading text
        
    Returns:
        HTML Node created based on input block
    '''

    prefix_hash_tag_counts = 0
    header_delimiter = BlockType.HEADING.value
  
    for c in block:
        if c == header_delimiter and prefix_hash_tag_counts <= 5:
            prefix_hash_tag_counts += 1
        else:
            break
    trailingEmptySpce = ' '
    prefixHeading = prefix_hash_tag_counts * BlockType.HEADING.value + trailingEmptySpce
    block_prefix_removed = block.removeprefix(prefixHeading)

    matching_html_header_tag = html_headinger_tag_dict[prefix_hash_tag_counts]

    return md_terminal_block_to_htmlNode(block_prefix_removed, htmlTag = matching_html_header_tag)


def md_coding_block_to_htmlNode(block:str):
    '''
    Parse a markdown coding block into htnl node. Note that coding blocks can't have nested inline elements

    Args:
        block: markdown coding block starting with ``` and ending with ```

    Returns:
        html node representing the coding block wrapped with <pre> 
    '''
    # strip() since \n always follows after  ``` in md code block 
    block_prefix_suffix_removed = block.removeprefix(BlockType.CODE.value).removesuffix(BlockType.CODE.value).strip()
    
    childNode = LeafNode( tag=Tag.CODE, value=block_prefix_suffix_removed)

    return ParentNode(tag = Tag.PREFORMATTED, children=[childNode])


def md_quote_block_to_htmlNode(block : str):
    '''
    Parse a quote block into html node
    
    Args:
        Markdown text starting with "> "

    Returns:
        Corresponding HTML node
    '''

    lines = block.splitlines()
    new_lines = []
    
    for line in lines:
        if line.startswith(">"):

            cleaned = line.lstrip(">").strip()
            new_lines.append(cleaned)
        else:
            new_lines.append(line)
            
    content = " ".join(new_lines)

    return md_terminal_block_to_htmlNode(content, htmlTag = Tag.QUOTE)

def md_unordered_list_block_to_htmlNode(block: str):
    '''
    Converts md block of unordered list into html node

    Args:
        block: md text of unordered list

    Returns:
        Parent html node with list items as children html node 
    '''

    lines = block.splitlines()
    unordered_list_item_md_text = []

    for line in lines:
        is_new_unordered_item = line.startswith(BlockType.UNORDERED_LIST.value) 
        
        if is_new_unordered_item:
            prefix_removed_line = line.removeprefix(BlockType.UNORDERED_LIST.value) 
            unordered_list_item_md_text.append(prefix_removed_line)

        if not is_new_unordered_item:
            unordered_list_item_md_text[-1] = unordered_list_item_md_text[-1] + "\n" + line


    children_html_node_list = []
    for unordered_item in unordered_list_item_md_text:
        unordered_item_html_node = md_terminal_block_to_htmlNode(unordered_item, Tag.LIST_ITEM)
        children_html_node_list.append(unordered_item_html_node)


    return ParentNode(tag = Tag.UNORDERED_LIST, children= children_html_node_list)



def md_ordered_list_block_to_htmlNode(block: str):
    '''
    Converts md block of ordered list into html node

    Args:
        block: md text of ordered list

    Returns:
        Parent html node with list items as children html node 
    '''

    item_md_text_list = []
    lines = block.splitlines()
    ordered_list_count = 1
    ordered_list_count_prefix = str(ordered_list_count) + ". "
    for line in lines:
        is_new_line_item = line.startswith(ordered_list_count_prefix)

        if is_new_line_item:
            prefix_removed_list_item = line.removeprefix(ordered_list_count_prefix)
            item_md_text_list.append(prefix_removed_list_item)

            ordered_list_count += 1
            ordered_list_count_prefix = str(ordered_list_count) + ". "
        
        else:
            item_md_text_list[-1] = item_md_text_list[-1] + "\n" + line

    children_list_htmlnode = []

    for item in item_md_text_list:
        item_html_node = md_terminal_block_to_htmlNode(item, htmlTag=Tag.LIST_ITEM)        
        children_list_htmlnode.append(item_html_node)

    return ParentNode(tag = Tag.ORDERED_LIST, children = children_list_htmlnode)



md = '''# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
'''

# if __name__ == "__main__":
#     block = """> "I am in fact a Hobbit in all but size."
# >
# > -- J.R.R. Tolkien"""

#     print(block_to_block_type(block))
#     print(block)
    # for b in splitted_blocks:
    #     print()
    #     print(b)
    #     print()

