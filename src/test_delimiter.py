import unittest
from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from extractmarkdown import markdown_to_blocks, block_to_html, markdown_to_html


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ])

    def test_bold(self):
        node = TextNode("Hello **world** today", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("world", TextType.BOLD),
            TextNode(" today", TextType.PLAIN),
        ])

    def test_italic(self):
        node = TextNode("Hello _world_ today", TextType.PLAIN)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("world", TextType.ITALIC),
            TextNode(" today", TextType.PLAIN),
        ])

    def test_non_plain_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.PLAIN),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("text at the end `code`", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("text at the end ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
        ])

    def test_multiple_delimiters(self):
        node = TextNode("a `b` c `d` e", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("a ", TextType.PLAIN),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.PLAIN),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.PLAIN),
        ])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This is `unclosed", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_mixed_node_list(self):
        nodes = [
            TextNode("plain `code` text", TextType.PLAIN),
            TextNode("already bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("plain ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.PLAIN),
            TextNode("already bold", TextType.BOLD),
        ])


class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode("text ![cat](https://example.com/cat.png) end", TextType.PLAIN)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("text ", TextType.PLAIN),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            TextNode(" end", TextType.PLAIN),
        ])

    def test_multiple_images(self):
        node = TextNode("![a](https://example.com/a.png) and ![b](https://example.com/b.png)", TextType.PLAIN)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("b", TextType.IMAGE, "https://example.com/b.png"),
        ])

    def test_image_at_start(self):
        node = TextNode("![cat](https://example.com/cat.png) some text", TextType.PLAIN)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            TextNode(" some text", TextType.PLAIN),
        ])

    def test_image_at_end(self):
        node = TextNode("some text ![cat](https://example.com/cat.png)", TextType.PLAIN)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("some text ", TextType.PLAIN),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
        ])

    def test_no_images(self):
        node = TextNode("just plain text", TextType.PLAIN)
        result = split_nodes_image([node])
        self.assertEqual(result, [TextNode("just plain text", TextType.PLAIN)])

    def test_non_plain_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])


class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        node = TextNode("text [click me](https://example.com) end", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("text ", TextType.PLAIN),
            TextNode("click me", TextType.LINK, "https://example.com"),
            TextNode(" end", TextType.PLAIN),
        ])

    def test_multiple_links(self):
        node = TextNode("[a](https://a.com) and [b](https://b.com)", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("a", TextType.LINK, "https://a.com"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("b", TextType.LINK, "https://b.com"),
        ])

    def test_link_at_start(self):
        node = TextNode("[click](https://example.com) some text", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("click", TextType.LINK, "https://example.com"),
            TextNode(" some text", TextType.PLAIN),
        ])

    def test_link_at_end(self):
        node = TextNode("some text [click](https://example.com)", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("some text ", TextType.PLAIN),
            TextNode("click", TextType.LINK, "https://example.com"),
        ])

    def test_no_links(self):
        node = TextNode("just plain text", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("just plain text", TextType.PLAIN)])

    def test_non_plain_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_image_not_matched_as_link(self):
        node = TextNode("![alt](https://example.com/img.png)", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("![alt](https://example.com/img.png)", TextType.PLAIN)])


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        result = text_to_textnodes("just plain text")
        self.assertEqual(result, [TextNode("just plain text", TextType.PLAIN)])

    def test_bold(self):
        result = text_to_textnodes("Hello **world**")
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("world", TextType.BOLD),
        ])

    def test_italic(self):
        result = text_to_textnodes("Hello _world_")
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("world", TextType.ITALIC),
        ])

    def test_code(self):
        result = text_to_textnodes("Hello `world`")
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("world", TextType.CODE),
        ])

    def test_image(self):
        result = text_to_textnodes("Hello ![cat](https://example.com/cat.png)")
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
        ])

    def test_link(self):
        result = text_to_textnodes("Hello [click](https://example.com)")
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("click", TextType.LINK, "https://example.com"),
        ])

    def test_all_types(self):
        result = text_to_textnodes(
            "plain **bold** _italic_ `code` ![img](https://example.com/img.png) [link](https://example.com)"
        )
        self.assertEqual(result, [
            TextNode("plain ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
        ])


class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_split(self):
        text = "first block\n\nsecond block"
        self.assertEqual(markdown_to_blocks(text), ["first block", "second block"])

    def test_three_blocks(self):
        text = "block one\n\nblock two\n\nblock three"
        self.assertEqual(markdown_to_blocks(text), ["block one", "block two", "block three"])

    def test_strips_whitespace(self):
        text = "  block one  \n\n  block two  "
        self.assertEqual(markdown_to_blocks(text), ["block one", "block two"])

    def test_multiple_blank_lines_between_blocks(self):
        text = "block one\n\n\n\nblock two"
        self.assertEqual(markdown_to_blocks(text), ["block one", "block two"])

    def test_multiline_block(self):
        text = "line one\nline two\n\nline three\nline four"
        self.assertEqual(markdown_to_blocks(text), ["line one\nline two", "line three\nline four"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_no_double_newline(self):
        text = "just one block"
        self.assertEqual(markdown_to_blocks(text), ["just one block"])


class TestBlockToHtml(unittest.TestCase):

    def test_paragraph(self):
        result = block_to_html("hello world")
        self.assertEqual(result.to_html(), "<p>hello world</p>")

    def test_heading_h1(self):
        result = block_to_html("# Heading one")
        self.assertEqual(result.to_html(), "<h1>Heading one</h1>")

    def test_heading_h3(self):
        result = block_to_html("### Heading three")
        self.assertEqual(result.to_html(), "<h3>Heading three</h3>")

    def test_code_block(self):
        result = block_to_html("```\nsome code\n```")
        self.assertEqual(result.to_html(), "<pre><code>some code</code></pre>")

    def test_quote(self):
        result = block_to_html("> a quote")
        self.assertEqual(result.to_html(), "<blockquote>a quote</blockquote>")

    def test_multiline_quote(self):
        result = block_to_html("> line one\n> line two")
        self.assertEqual(result.to_html(), "<blockquote>line one\nline two</blockquote>")

    def test_quote_with_empty_line(self):
        result = block_to_html('> "I am a Hobbit"\n>\n> -- Tolkien')
        self.assertEqual(result.to_html(), '<blockquote>"I am a Hobbit"\n\n-- Tolkien</blockquote>')

    def test_unordered_list(self):
        result = block_to_html("- item one\n- item two")
        self.assertEqual(result.to_html(), "<ul><li>item one</li><li>item two</li></ul>")

    def test_ordered_list(self):
        result = block_to_html("1. first\n2. second")
        self.assertEqual(result.to_html(), "<ol><li>first</li><li>second</li></ol>")

    def test_paragraph_with_inline_bold(self):
        result = block_to_html("hello **world**")
        self.assertEqual(result.to_html(), "<p>hello <b>world</b></p>")

    def test_paragraph_with_inline_link(self):
        result = block_to_html("visit [boot.dev](https://boot.dev)")
        self.assertEqual(result.to_html(), '<p>visit <a href="https://boot.dev">boot.dev</a></p>')


class TestMarkdownToHtml(unittest.TestCase):

    def test_single_paragraph(self):
        result = markdown_to_html("hello world")
        self.assertEqual(result.to_html(), "<div><p>hello world</p></div>")

    def test_multiple_blocks(self):
        result = markdown_to_html("# Title\n\na paragraph")
        self.assertEqual(result.to_html(), "<div><h1>Title</h1><p>a paragraph</p></div>")

    def test_full_document(self):
        md = "# Title\n\nA paragraph with **bold**.\n\n- item one\n- item two"
        result = markdown_to_html(md)
        self.assertEqual(
            result.to_html(),
            "<div><h1>Title</h1><p>A paragraph with <b>bold</b>.</p><ul><li>item one</li><li>item two</li></ul></div>"
        )


if __name__ == "__main__":
    unittest.main()
