import unittest

from conversions import *
from textnode import *
from htmlnode import *
from leafnode import *


class TestConversions(unittest.TestCase):
    def test_text_to_html(self):
        node = text_node_to_html_node(TextNode("This is a text node", "text"))
        node2 = LeafNode(None, "This is a text node")
        self.assertEqual(node, node2)

    def test_text_to_html_bold(self):
        node = text_node_to_html_node(TextNode("This is a text node", "bold"))
        node2 = LeafNode("b", "This is a text node")
        self.assertEqual(node, node2)
    
    def test_text_to_html_italic(self):
        node = text_node_to_html_node(TextNode("This is a text node", "italic"))
        node2 = LeafNode("i", "This is a text node")
        self.assertEqual(node, node2)
    
    def test_text_to_html_code(self):
        node = text_node_to_html_node(TextNode("This is a text node", "code"))
        node2 = LeafNode("code", "This is a text node")
        self.assertEqual(node, node2)
    
    def test_text_to_html_link(self):
        node = text_node_to_html_node(TextNode("This is a text node", "link", "www.google.com"))
        print(node)
        node2 = LeafNode("a", "This is a text node", {"href":"www.google.com"})
        self.assertEqual(node, node2)

    def test_text_to_html_image(self):
        node = text_node_to_html_node(TextNode("This is a text node", "image", "www.google.com"))
        node2 = LeafNode("img", None, {"src":"www.google.com", "alt":"This is a text node"})
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()