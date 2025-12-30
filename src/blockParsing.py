


def markdown_to_blocks(markdown_text):

    resultant_blocks = []

    splitted_parts = markdown_text.split("\n\n")

    for part in splitted_parts:
        part_stripped = part.strip()
        if not part:
            continue
        resultant_blocks.append(part_stripped)
    
    return resultant_blocks

