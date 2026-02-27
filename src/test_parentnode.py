import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
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
    
    def test_to_html_without_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_many_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        leaf_node = LeafNode(None, "normal text")
        leaf_node2 = LeafNode("b", "bold text")
        parent_node = ParentNode("p", [child_node, leaf_node, leaf_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><span><b>grandchild</b></span>normal text<b>bold text</b></p>"
        )

if __name__ == "__main__":
    unittest.main()