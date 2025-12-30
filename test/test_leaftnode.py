import unittest

from leafnode import Tag, tagOpeningRendering, tagClosingRendering, LeafNode

def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


def test_leaf_to_html_header_1(self):
    node = LeafNode("h1", "What's up!")
    self.assertEqual(node.to_html(), "<h1>What's up!</h>")


def test_leaf_to_html_hyperlink(self):
    node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
    self.assertEqual(node.to_html(), 
                     "<a href=\"https://www.google.com\">Click me!</a>"
                     )



