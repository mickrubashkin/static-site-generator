import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
