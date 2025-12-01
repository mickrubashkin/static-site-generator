import unittest

from build_content import extract_title

class TestBuildContent(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")
        md = "  #  Tolkien"
        self.assertEqual(extract_title(md), "Tolkien")
        md = "text\n# Title\nxx"
        self.assertEqual(extract_title(md), "Title")
        with self.assertRaises(Exception):
            extract_title("## Not an H1")
