import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("a", "bold", {"href": "https://www.google.com", "target": "_blank",})
        node2 = LeafNode("a", "bold", {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = LeafNode("a", "bold")
        node2 = LeafNode("a", "bold", None)
        self.assertEqual(node, node2)
    
    def test__not_eq(self):
        node = LeafNode("a", "bold", {"href": "https://www.google.com", "target": "_blank",})
        node2 = LeafNode("a", "bald", {"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node, node2)

    def test__not_eq2(self):
        node = LeafNode("a", "bold", {"href": "https://www.google.com", "target": "_blank",})
        node2 = LeafNode("a", "bald", {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)
    
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        
        html = node.to_html()

        self.assertEqual(html, '<p>This is a paragraph of text.</p>')
    
    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        
        html = node.to_html()

        self.assertEqual(html, '<a href="https://www.google.com">Click me!</a>')


if __name__ == "__main__":
    unittest.main()