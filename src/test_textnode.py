import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def tests_more_eq(self):
        node = TextNode("Can we get things to look code like...", TextType.CODE)
        node2 = TextNode("This test will pass if it rates things as different", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_testing(self):
        node = TextNode("Testing away through a buncha tests", TextType.LINK, None)
        node2 = TextNode("Testing away through a buncha tests", TextType.LINK)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()