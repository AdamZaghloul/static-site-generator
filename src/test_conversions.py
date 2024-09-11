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
        node2 = LeafNode("a", "This is a text node", {"href":"www.google.com"})
        self.assertEqual(node, node2)

    def test_text_to_html_image(self):
        node = text_node_to_html_node(TextNode("This is a text node", "image", "www.google.com"))
        node2 = LeafNode("img", None, {"src":"www.google.com", "alt":"This is a text node"})
        self.assertEqual(node, node2)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        new_nodes2 = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(new_nodes, new_nodes2)
    def test_split_nodes_delimiter_do_nothing(self):
        node = TextNode("This is a code block", "code")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        new_nodes2 = [
            TextNode("This is a code block", "code")
        ]
        self.assertEqual(new_nodes, new_nodes2)
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        
        new_nodes2 = [
            TextNode("This is text with a ", "text"),
            TextNode("bold", "bold"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(new_nodes, new_nodes2)
    def test_split_nodes_delimiter_italics(self):
        node = TextNode("This is text with an *italicyzed* word", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italics")
        
        new_nodes2 = [
            TextNode("This is text with an ", "text"),
            TextNode("italicyzed", "italics"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(new_nodes, new_nodes2)
    
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = extract_markdown_images(text)

        node2 = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(node, node2)
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = extract_markdown_links(text)

        node2 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(node, node2)
    
    def test_split_nodes_image(self):
        node = TextNode("This is text with an image called ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", "text")
        
        nodes = split_nodes_image([node])
        nodes2 = [
            TextNode("This is text with an image called ", "text"),
            TextNode("to boot dev", "image", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "image", "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(nodes, nodes2)
    def test_split_nodes_image2(self):
        node = TextNode("![to boot dev](https://www.boot.dev)This is text with an image called and ![to youtube](https://www.youtube.com/@bootdotdev)", "text")
        
        nodes = split_nodes_image([node])
        nodes2 = [
            TextNode("to boot dev", "image", "https://www.boot.dev"),
            TextNode("This is text with an image called and ", "text"),
            TextNode("to youtube", "image", "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(nodes, nodes2)
    def test_split_nodes_image3(self):
        node = TextNode("This is text with an image called ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) with text at the end.", "text")
        
        nodes = split_nodes_image([node])
        nodes2 = [
            TextNode("This is text with an image called ", "text"),
            TextNode("to boot dev", "image", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "image", "https://www.youtube.com/@bootdotdev"),
            TextNode(" with text at the end.", "text")
        ]
        self.assertEqual(nodes, nodes2)

    def test_split_nodes_link(self):
        node = TextNode("This is text with an image called [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        
        nodes = split_nodes_link([node])
        nodes2 = [
            TextNode("This is text with an image called ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(nodes, nodes2)
    def test_split_nodes_link2(self):
        node = TextNode("[to boot dev](https://www.boot.dev)This is text with an image called and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        
        nodes = split_nodes_link([node])
        nodes2 = [
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode("This is text with an image called and ", "text"),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(nodes, nodes2)
    def test_split_nodes_link3(self):
        node = TextNode("This is text with an image called [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with text at the end.", "text")
        
        nodes = split_nodes_link([node])
        nodes2 = [
            TextNode("This is text with an image called ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev"),
            TextNode(" with text at the end.", "text")
        ]
        self.assertEqual(nodes, nodes2)
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        nodes = text_to_textnodes(text)
        nodes2 = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(nodes, nodes2)
    
if __name__ == "__main__":
    unittest.main()