import unittest

from conversions import *
from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *


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
    
    def test_markdown_to_blocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        output = markdown_to_blocks(text)
        expected = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(output, expected)
    
    def test_block_to_block_type_paragrah(self):
        text = "This is a paragraph. Nice and simple."

        self.assertEqual(block_to_block_type(text), "paragraph")
    def test_block_to_block_type_heading1(self):
        text = "#This is a heading"

        self.assertEqual(block_to_block_type(text), "heading")
    def test_block_to_block_type_heading2(self):
        text = "##This is a heading"

        self.assertEqual(block_to_block_type(text), "heading")
    def test_block_to_block_type_heading3(self):
        text = "###This is a heading"

        self.assertEqual(block_to_block_type(text), "heading")
    def test_block_to_block_type_heading4(self):
        text = "####This is a heading"

        self.assertEqual(block_to_block_type(text), "heading")
    def test_block_to_block_type_heading5(self):
        text = "#####This is a heading"

        self.assertEqual(block_to_block_type(text), "heading")
    def test_block_to_block_type_heading6(self):
        text = "######This is a heading"

        self.assertEqual(block_to_block_type(text), "heading")
    def test_block_to_block_type_code(self):
        text = "```This is a one-line code block```"

        self.assertEqual(block_to_block_type(text), "code")
    def test_block_to_block_type_code2(self):
        text = "```This is a\ntwo-line code block```"

        self.assertEqual(block_to_block_type(text), "code")
    def test_block_to_block_type_quote(self):
        text = ">This is a one-line quote"

        self.assertEqual(block_to_block_type(text), "quote")
    def test_block_to_block_type_quote2(self):
        text = ">This is a \n>two-line quote"

        self.assertEqual(block_to_block_type(text), "quote")
    def test_block_to_block_type_ul(self):
        text = "- This is a one-line ul"

        self.assertEqual(block_to_block_type(text), "unordered_list")
    def test_block_to_block_type_ul2(self):
        text = "- This is a\n- two-line ul"

        self.assertEqual(block_to_block_type(text), "unordered_list")
    def test_block_to_block_type_ul3(self):
        text = "- This is a\n* two-line mixed ul"

        self.assertEqual(block_to_block_type(text), "unordered_list")
    def test_block_to_block_type_ol(self):
        text = "1. This is a one-line ol"

        self.assertEqual(block_to_block_type(text), "ordered_list")
    def test_block_to_block_type_ol2(self):
        text = "1. This\n2. is\n3. a\n4. multi-line\n5. ol"

        self.assertEqual(block_to_block_type(text), "ordered_list")
    def test_block_to_block_type_code_error(self):
        text = "```This is a one-line code block``"

        self.assertEqual(block_to_block_type(text), "paragraph")
    def test_block_to_block_type_quote_error(self):
        text = ">This is a \ntwo-line quote"

        self.assertEqual(block_to_block_type(text), "paragraph")
    def test_block_to_block_type_ul_error(self):
        text = "- This is a\ntwo-line ul"

        self.assertEqual(block_to_block_type(text), "paragraph")
    def test_block_to_block_type_ol_error(self):
        text = "1. This\n2. is\n4. a\n4. multi-line\n5. ol"

        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_markdown_to_html_node_heading(self):
        text = "###This is a heading3"

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("h3", [LeafNode(None, text[3:], None)], None)], None)

        self.assertEqual(node, node2)
    def test_markdown_to_html_node_heading2(self):
        text = "###This is a heading3 with a **bold** word"

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("h3", [LeafNode(None, "This is a heading3 with a ", None), LeafNode("b", "bold", None), LeafNode(None, " word", None)], None)], None)

        self.assertEqual(node, node2)
    def test_markdown_to_html_node_code(self):
        text = "```This is a code block with a **bold** word```"

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("pre", [ParentNode("code", [LeafNode(None, "This is a code block with a ", None), LeafNode("b", "bold", None), LeafNode(None, " word", None)], None)], None)], None)
        self.assertEqual(node, node2)

    def test_markdown_to_html_node_quote(self):
        text = ">This is a single line quote with a **bold** word"

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("blockquote", [LeafNode(None, "This is a single line quote with a ", None), LeafNode("b", "bold", None), LeafNode(None, " word", None)], None)], None)
        self.assertEqual(node, node2)
    def test_markdown_to_html_node_quote2(self):
        text = ">This is a multi\n>line quote with a **bold** word"

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("blockquote", [LeafNode(None, "This is a multi\nline quote with a ", None), LeafNode("b", "bold", None), LeafNode(None, " word", None)], None)], None)
        self.assertEqual(node, node2)
    def test_markdown_to_html_node_list_ol(self):
        text = "1. This\n2. is\n3. an\n4. ordered\n5. list with a **bold** word"

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("ol", [ParentNode("li", [LeafNode(None, "This", None)], None), ParentNode("li", [LeafNode(None, "is", None)], None), ParentNode("li", [LeafNode(None, "an", None)], None), ParentNode("li", [LeafNode(None, "ordered", None)], None), ParentNode("li", [LeafNode(None, "list with a ", None), LeafNode("b", "bold", None), LeafNode(None, " word", None)], None)], None)], None)
        self.assertEqual(node, node2)

    def test_markdown_to_html_node_list_ul(self):
        text = "- This\n* is\n- an\n* unordered\n- list with a **bold** word"

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("ul", [ParentNode("li", [LeafNode(None, "This", None)], None), ParentNode("li", [LeafNode(None, "is", None)], None), ParentNode("li", [LeafNode(None, "an", None)], None), ParentNode("li", [LeafNode(None, "unordered", None)], None), ParentNode("li", [LeafNode(None, "list with a ", None), LeafNode("b", "bold", None), LeafNode(None, " word", None)], None)], None)], None)
        self.assertEqual(node, node2)

    def test_markdown_to_html_node_paragraph(self):
        text = "This is a paragraph with a **bold** and *italic* word."

        node = markdown_to_html_node(text)
        node2 = ParentNode("div", [ParentNode("p", [LeafNode(None, "This is a paragraph with a ", None), LeafNode("b", "bold", None), LeafNode(None, " and ", None), LeafNode("i", "italic", None), LeafNode(None, " word.", None)], None)], None)   
        self.assertEqual(node, node2)
    
    def test_extract_title(self):
        text = "# Hello "

        title = "Hello"

        self.assertEqual(extract_title(text), title)
    
    def test_extract_title2(self):
        text = "## Hi\n#Hello\nthis is a line"

        title = "Hello"

        self.assertEqual(extract_title(text), title)

if __name__ == "__main__":
    unittest.main()