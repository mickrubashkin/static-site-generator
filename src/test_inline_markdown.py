import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_positive(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i in range(len(new_nodes)):
            new_node = new_nodes[i]
            expected_node = expected_nodes[i]
            self.assertEqual(new_node.text, expected_node.text)
            self.assertEqual(new_node.text_type, expected_node.text_type)

    def test_raises_on_unmatched_delimiter(self):
        node = TextNode("this is `broken code", TextType.TEXT)

        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertIn("INVALID MARKDOWN", str(cm.exception))
