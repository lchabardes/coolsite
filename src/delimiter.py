from textnode import TextNode, TextType
import re


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\s\)]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\s\)]+)\)"
    return re.findall(pattern, text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: no closing '{delimiter}' delimiter in '{node.text}'")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for alt, url in images:
            sections = remaining.split(f"![{alt}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.PLAIN))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for text, url in links:
            sections = remaining.split(f"[{text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.PLAIN))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
