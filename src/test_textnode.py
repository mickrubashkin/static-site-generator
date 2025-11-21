import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, link, https://www.boot.dev)", repr(node))


if __name__ == "__main__":
    unittest.main()
