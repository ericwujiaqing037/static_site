
#######

<blockquote>This is a quote.</blockquote>

### To-Do List
- [x] Create HTMLNode class
- [x] Create LeafNode class
- [ ] Handle empty "props" in Image tags
- [ ] Write unit tests

### Supported Tags
1. Paragraph (`p`)
2. Link (`a`)
3. Image (`img`)

Click here to learn about [Recursion](https://en.wikipedia.org/wiki/Recursion).

![Warning Icon](https://via.placeholder.com/150/FF0000/FFFFFF?text=Warning)



# Static Site Generator

## Overview
This project generates HTML from **Python objects**. It handles various tags and ensures data safety.

## Classes
* `HTMLNode`: The base class.
* `LeafNode`: Represents elements without children (e.g., `<b>`, `<img>`).

## Usage
```python
node = LeafNode(Tag.IMG, "", {"src": "cat.jpg", "alt": "A cute cat"})
print(node.to_html())

Act as my programming mentor who is interested in nurturing me into the best programmer possible. Don’t spoon feed me, don’t show me the direct answers, only nudge me in the right direction.

Context: right now, i am trying to build a parser that converts markdown language into html. The main challenge I face is in handling the nesting structures & sequential orderings

Example Input:
### To-Do List
- [x] Create HTMLNode class
- [x] Create LeafNode class
- [ ] Handle empty "props" in Image tags
- [ ] Write unit tests

### Supported Tags
1. Paragraph (`p`)
2. Link (`a`)
3. Image (`img`)

This should split into:
HTML Node:
   HTML Node: Header: ### To-Do List
   HTML Node: To-Do List
     4 leaf nodes -> corresponding to 4 options
   HTML Node: Header: ### Supported Tags
   HTML Node: Supported Tags
      3 leaft nodes -> corresponding to 3 options

Suppose that I 

Decomposition: nesting structure

Overall Sequence:
Markdown -> Split by blocks -> blocks to text node -> text node 
-> html node -> leaf nodes -> renders into htmls

Input: mark down text
Output: a single html node


Steps:
1) split markdown into blocks -> sequential order already stored in list
2) for each block -> determine block type -> corresponding html node
    3) create a html node 
    Cases:
        heading -> 
            determine which level of heading h1 to h6
            create textnode of text type 
        
        code ->

        quote ->

        ordered list ->

        unorered list ->

        paragraph ->


Split by blocks:
# Paragraph / Headings / Code / Quote / Order list / Unorderd list
  - each of these blocks can serve as a parent or leaf HTML node
  - enforce:
      - parent node strictly no value 
      - leaf node must have value & renders


Should be traversal by bfs -> on each level 

each block should represent a html node 



leafnode -> converts into html /renders

What is the relationship between text node and leaf node?


text node -> parsing
leaf node -> strictly rendering 