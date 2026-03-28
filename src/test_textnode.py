import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url(self):
        node = TextNode("First link", TextType.PLAIN)
        self.assertEqual(node.url, None)
    def test_text_type(self):
        with self.assertRaises(ValueError):
            TextNode("Some text", "invalidType")
    def test_relative_url(self):
        node = TextNode("Some text", TextType.LINK, "/images/glorfindel.png")
        self.assertEqual(node.url, "/images/glorfindel.png")

    def test_absolute_url(self):
        node = TextNode("Some text", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")



    def test_text_node_to_html_image(self):
        node = TextNode("a cat", TextType.IMAGE, "https://example.com/cat.png")
        leaf = node.text_node_to_html(node)
        self.assertEqual(leaf.to_html(), '<img src="https://example.com/cat.png" alt="a cat"></img>')

    def test_text_node_to_html_link(self):
        node = TextNode("click me", TextType.LINK, "https://example.com")
        leaf = node.text_node_to_html(node)
        self.assertEqual(leaf.to_html(), '<a href="https://example.com">click me</a>')

    def test_text_node_to_html_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        leaf = node.text_node_to_html(node)
        self.assertEqual(leaf.to_html(), "<b>bold text</b>")

    def test_text_node_to_html_plain(self):
        node = TextNode("plain text", TextType.PLAIN)
        leaf = node.text_node_to_html(node)
        self.assertEqual(leaf.to_html(), "plain text")

if __name__ == "__main__":
    unittest.main()