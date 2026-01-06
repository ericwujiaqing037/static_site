import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    # def test_eq(self):
    #     node = HTMLNode("h1", "This is a HTML text")
    #     node2 = HTMLNode("h1", "This is a HTML text")
    #     self.assertEqual(node, node2)

    def test_eq_false(self):
        node = HTMLNode("h1", "This is a HTML text")
        node2 = HTMLNode("h2", "This is a HTML text")
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = HTMLNode("h1", "This is a HTML text")
        node2 = HTMLNode("h1", "This is not a HTML text")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()


import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_header_1(self):
        node = LeafNode("h1", "What's up!")
        self.assertEqual(node.to_html(), "<h1>What's up!</h>")


    def test_leaf_to_html_hyperlink(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), 
                        "<a href=\"https://www.google.com\">Click me!</a>")

if __name__ == "__main__":
    unittest.main()
