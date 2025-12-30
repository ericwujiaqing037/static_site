from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "- "
    ORDERED_LIST = ". "


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
        heading = "#" * i + " "
        if block.startswith(heading):
            # blockText = block.removeprefix(heading)
            return BlockType.HEADING

    # check code block
    if len(block) >= 6 and block.startswith(BlockType.CODE.value) and block.endswith(BlockType.CODE.value):
        # blockText = block.removeprefix(BlockType.CODE.value)
        # blockText = blockText.removepostfix(BlockType.CODE.value)
        return BlockType.CODE
    
    quotedBlocks = True
    unorderedList = True
    orderedList = True

    splitted_blocks = block.split("\n")

    for index, b in enumerate(splitted_blocks):
        if b and not b.startswith(BlockType.QUOTE.value):
            quotedBlocks = False

        if b and not b.startswith(BlockType.UNORDERED_LIST.value):
            unorderedList = False

        if b and not b.startswith(str(index + 1) + BlockType.ORDERED_LIST.value):
            orderedList = False

        if not quotedBlocks and not unorderedList and not orderedList:
            break

    if quotedBlocks:
        return BlockType.QUOTE
    
    if unorderedList:
        return BlockType.UNORDERED_LIST

    if orderedList:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown_text):
    '''
    converts full markdown document into a single parent HTML node
    '''
    pass