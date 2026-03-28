from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    ITALIC = "italic"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise ValueError(f"Invalid text_type: {text_type!r}. Must be a TextType enum member.")
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html(self, text_node):
        if text_node.text_type == TextType.PLAIN:
            return LeafNode(None, text_node.text, None)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text, None)
        elif text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")
        
