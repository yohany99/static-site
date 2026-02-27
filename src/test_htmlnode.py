import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        attr = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=attr)
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())
    
    def test_repr(self):
        node = HTMLNode("p", "Hello, world!", None, {"class": "primary"})
        self.assertEqual("HTMLNode(p, Hello, world!, children: None, {'class': 'primary'})", repr(node))
    
    def test_props_to_html2(self):
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual("", node.props_to_html())

    def test_values(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

if __name__ == "__main__":
    unittest.main()