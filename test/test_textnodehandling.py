import unittest

from textnode import *
from textnodeParsing import *


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class TestTextNodeSplitbyDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        old_node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        split_results = split_nodes_delimiter([old_node], DELIMITER_MAP[TextType.BOLD], TextType.BOLD)
        
        self.assertEqual(split_results[0], TextNode("This is text with a ",TextType.TEXT))
        self.assertEqual(split_results[1], TextNode("bolded phrase",TextType.BOLD))
        self.assertEqual(split_results[2], TextNode(" in the middle",TextType.TEXT))
        
    def test_split_nodes_delimiter_italic(self):
        old_node = TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT)
        split_results = split_nodes_delimiter([old_node], DELIMITER_MAP[TextType.ITALIC], TextType.ITALIC)
        
        self.assertEqual(split_results[0], TextNode("This is text with a ",TextType.TEXT))
        self.assertEqual(split_results[1], TextNode("italic phrase",TextType.ITALIC))
        self.assertEqual(split_results[2], TextNode(" in the middle",TextType.TEXT))

class TestHTMLNode(unittest.TestCase):
    def test_extracting_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_regular_links(self):
        matches = extract_regular_links("Testing Eample[Click here to visit Example](https://www.example.com)")
        
        self.assertListEqual( [("Click here to visit Example", "https://www.example.com")], matches)


class TestTextNodeSplitbyImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestTextNodeSplitbyLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [first url](https://i.imgur.com/zjjcJKZ.png) and another [second url](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("first url", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second url", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        resultant_nodes = text_to_textnodes(text)
        self.assertEqual(
            resultant_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )