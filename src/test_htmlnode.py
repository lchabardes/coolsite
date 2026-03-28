import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

# Sample nodes to reuse across tests
link_node   = HTMLNode("a", "click me", props={"href": "https://example.com", "target": "_blank"})
plain_node  = HTMLNode("p", "hello world")
parent_node = HTMLNode("div", children=[plain_node, link_node])
empty_node  = HTMLNode()

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        # attributes render in key="value" format
        result = link_node.props_to_html()
        self.assertIn('href="https://example.com"', result)
        self.assertIn('target="_blank"', result)

    def test_props_to_html_no_props(self):
        # node with no props returns empty string (or just whitespace)
        result = plain_node.props_to_html()
        self.assertEqual(result.strip(), "")

    def test_repr(self):
        # repr includes tag and value
        result = repr(plain_node)
        self.assertIn("p", result)
        self.assertIn("hello world", result)

    def test_children(self):
        self.assertEqual(len(parent_node.children), 2)

    def test_defaults_are_none(self):
        self.assertIsNone(empty_node.tag)
        self.assertIsNone(empty_node.value)
        self.assertIsNone(empty_node.children)
        self.assertIsNone(empty_node.props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_children(self):
        node = LeafNode("p", "Hello")
        self.assertIsNone(node.children)

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "click me", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">click me</a>')

    def test_leaf_to_html_no_tag(self):
        # no tag = raw text, no wrapping elements
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_with_props(self):
        node = ParentNode("div", [LeafNode("p", "text")], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>text</p></div>')

    def test_parent_multiple_children(self):
        node = ParentNode("ul", [
            LeafNode("li", "one"),
            LeafNode("li", "two"),
            LeafNode("li", "three"),
        ])
        self.assertEqual(node.to_html(), "<ul><li>one</li><li>two</li><li>three</li></ul>")

    def test_parent_value_is_none(self):
        node = ParentNode("div", [LeafNode("p", "text")])
        self.assertIsNone(node.value)
