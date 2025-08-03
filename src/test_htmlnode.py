import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "Test to test go brr", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        }
    )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html2(self):
        node = HTMLNode("p", "Test to test go brr", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("a", "link", None, {"href": "https://boot.dev"})
        output = repr(node)
        self.assertIn("a", output)
        self.assertIn("link", output)
        self.assertIn("href", output)

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "testing away")
        self.assertEqual(node.to_html(), "testing away")

    def test_leaf_to_html_link(self):
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_errortest(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

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

