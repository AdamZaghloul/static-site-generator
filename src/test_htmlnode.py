import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "bold", [], {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("a", "bold", [], {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("a", "bold", [], None)
        node2 = HTMLNode("a", "bold", [])
        self.assertEqual(node, node2)
    
    def test__not_eq(self):
        node = HTMLNode("a", "bold", [], {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("a", "bold", [], {"href": "https://www.google.com", "target": "_not_blank",})
        self.assertNotEqual(node, node2)

    def test__not_eq2(self):
        node = HTMLNode("a", "bold", [], {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("a", "bold", [node], {"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node, node2)
    
    def test_props_to_html(self):
        node = HTMLNode("a", "bold", [], {"href": "https://www.google.com", "target": "_blank"})
        
        html = node.props_to_html()

        self.assertEqual(html, 'href="https://www.google.com" target="_blank"')
    
    def test_props_to_html2(self):
        node = HTMLNode("a", "bold", [])
        
        html = node.props_to_html()

        self.assertEqual(html, '')


if __name__ == "__main__":
    unittest.main()