import unittest
from extractmarkdown import block_to_block_type, BlockType, extract_title
from delimiter import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_image(self):
        text = "![a cat](https://example.com/cat.png)"
        self.assertEqual(extract_markdown_images(text), [("a cat", "https://example.com/cat.png")])

    def test_multiple_images(self):
        text = "![cat](https://example.com/cat.png) and ![dog](https://example.com/dog.png)"
        self.assertEqual(extract_markdown_images(text), [
            ("cat", "https://example.com/cat.png"),
            ("dog", "https://example.com/dog.png"),
        ])

    def test_empty_alt_text(self):
        text = "![](https://example.com/cat.png)"
        self.assertEqual(extract_markdown_images(text), [("", "https://example.com/cat.png")])

    def test_no_images(self):
        text = "just plain text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_link_not_matched_as_image(self):
        text = "[not an image](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_image_mixed_with_text(self):
        text = "Here is an image ![alt](https://example.com/img.png) in a sentence."
        self.assertEqual(extract_markdown_images(text), [("alt", "https://example.com/img.png")])


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_single_link(self):
        text = "[click me](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("click me", "https://example.com")])

    def test_multiple_links(self):
        text = "[google](https://google.com) and [boot.dev](https://boot.dev)"
        self.assertEqual(extract_markdown_links(text), [
            ("google", "https://google.com"),
            ("boot.dev", "https://boot.dev"),
        ])

    def test_empty_anchor_text(self):
        text = "[](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("", "https://example.com")])

    def test_no_links(self):
        text = "just plain text"
        self.assertEqual(extract_markdown_links(text), [])

    def test_image_not_matched_as_link(self):
        text = "![alt](https://example.com/img.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_mixed_with_text(self):
        text = "Visit [boot.dev](https://boot.dev) to learn more."
        self.assertEqual(extract_markdown_links(text), [("boot.dev", "https://boot.dev")])


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading one"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Heading three"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading six"), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        # 7 hashes is not a valid heading
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> this is a quote"), BlockType.QUOTE)

    def test_multiline_quote(self):
        self.assertEqual(block_to_block_type("> line one\n> line two"), BlockType.QUOTE)

    def test_quote_with_empty_line(self):
        self.assertEqual(block_to_block_type('> "I am a Hobbit"\n>\n> -- Tolkien'), BlockType.QUOTE)

    def test_unordered_list_dash(self):
        self.assertEqual(block_to_block_type("- item one\n- item two"), BlockType.UNORDERED_LIST)

    def test_unordered_list_asterisk(self):
        self.assertEqual(block_to_block_type("* item one\n* item two"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just a normal paragraph"), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)

    def test_mixed_quote_and_plain(self):
        self.assertEqual(block_to_block_type("> quote line\nnot a quote"), BlockType.PARAGRAPH)

    def test_mixed_unordered_list_and_plain(self):
        self.assertEqual(block_to_block_type("- item one\nnot a list item"), BlockType.PARAGRAPH)

    def test_mixed_ordered_list_and_plain(self):
        self.assertEqual(block_to_block_type("1. first\nnot a list item"), BlockType.PARAGRAPH)

    def test_unclosed_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code without closing"), BlockType.PARAGRAPH)

    def test_ordered_list_skipped_number(self):
        self.assertEqual(block_to_block_type("1. first\n3. skipped two"), BlockType.ORDERED_LIST)


class TestExtractTitle(unittest.TestCase):

    def test_simple_title(self):
        self.assertEqual(extract_title("# My Title"), "My Title")

    def test_title_among_other_blocks(self):
        md = "# My Title\n\nsome paragraph\n\n## Not the title"
        self.assertEqual(extract_title(md), "My Title")

    def test_h2_not_treated_as_title(self):
        with self.assertRaises(ValueError):
            extract_title("## Not a title")

    def test_no_heading_raises(self):
        with self.assertRaises(ValueError):
            extract_title("just a paragraph")

    def test_title_not_first_block(self):
        md = "some paragraph\n\n# Title later"
        self.assertEqual(extract_title(md), "Title later")


if __name__ == "__main__":
    unittest.main()
