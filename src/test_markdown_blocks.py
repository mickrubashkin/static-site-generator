import unittest
from src.markdown_blocks import markdown_to_blocks

class TestBlocksMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph(self):
        md = "Just a single paragraph with **bold** text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with **bold** text."])

    def test_leading_and_trailing_blank_lines(self):
        md = """

First block

Second block

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_multiple_blank_lines_between_blocks(self):
        md = """First block


Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["First block", "Second block", "Third block"],
        )

    def test_list_and_paragraph(self):
        md = """
- item 1
- item 2

A paragraph after the list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- item 1\n- item 2", "A paragraph after the list"],
        )

if __name__ == "__main__":
    unittest.main()
