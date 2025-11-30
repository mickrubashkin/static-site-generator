import unittest
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node

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

    def test_block_heading(self):
        self.assertEqual(block_to_block_type("# Heading1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# # Strange but still heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# "), BlockType.HEADING)

    def test_block_code(self):
        self.assertEqual(block_to_block_type("```some code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```some code\n\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```para"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("``para```"), BlockType.PARAGRAPH)

    def test_block_quote(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">quote\n>quote\n>quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">quote\n>quote\nnot quote"), BlockType.PARAGRAPH)

    def test_block_unordered_list(self):
        self.assertEqual(block_to_block_type("- unordered list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- unordered list\n- unordered list\n- unordered list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- unordered list\n- unordered list\nnot list"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-not unordered list"), BlockType.PARAGRAPH)

    def test_block_ordered_list(self):
        self.assertEqual(block_to_block_type("1. ordered list"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. ordered list\n2. ordered list\n3. ordered list"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. ordered list\n3. not ordered"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1 not ordered list"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. not ordered list"), BlockType.PARAGRAPH)

    def test_block_paragraph(self):
        self.assertEqual(block_to_block_type("some regular para text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("some regular para text\n>para\n```para```\n>para"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"

        self.assertEqual(html, expected_html)

    def test_headings(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

        md = "# This is a _heading_ with **inline** `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <i>heading</i> with <b>inline</b> <code>code</code></h1></div>",
        )

        md = """
# Title

## Subtitle _here_

### Third **level**
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><h2>Subtitle <i>here</i></h2><h3>Third <b>level</b></h3></div>"
        )

    def test_quote_block(self):
        md = """
> This is a _quoted_ line
> that spans **multiple** lines
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <i>quoted</i> line that spans <b>multiple</b> lines</blockquote></div>",
        )

    def test_ordered_list_simple(self):
        md = """
1. First item
2. Second item with _italic_
3. Third item with **bold**
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol>"
            "<li>First item</li>"
            "<li>Second item with <i>italic</i></li>"
            "<li>Third item with <b>bold</b></li>"
            "</ol></div>",
        )

    def test_unordered_list_simple(self):
        md = """
- First item
- Second item with _italic_
- Third item with **bold**
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul>"
            "<li>First item</li>"
            "<li>Second item with <i>italic</i></li>"
            "<li>Third item with <b>bold</b></li>"
            "</ul></div>",
        )



if __name__ == "__main__":
    unittest.main()
