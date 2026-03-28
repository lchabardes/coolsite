import re
import os
from enum import Enum
from htmlnode import ParentNode, LeafNode
from delimiter import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if re.fullmatch(r'#{1,6} .+', block):
        return BlockType.HEADING
    if re.fullmatch(r'```[\s\S]*```', block):
        return BlockType.CODE
    if re.fullmatch(r'(?:>.*\n?)+', block):
        return BlockType.QUOTE
    if re.fullmatch(r'(?:[-*+] .+\n?)+', block):
        return BlockType.UNORDERED_LIST
    if re.fullmatch(r'(?:\d+\. .+\n?)+', block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def get_heading_level(block):
    count = len(block) - len(block.lstrip('#'))
    return count if 1 <= count <= 6 else None


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    no_wp = []
    for block in blocks:
        if block.strip() == "":
            continue
        else:
            no_wp.append(block.strip())
    return no_wp


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [node.text_node_to_html(node) for node in text_nodes]


def block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", text_to_children(block))

    if block_type == BlockType.HEADING:
        heading_level = get_heading_level(block)
        stripped_block = block[heading_level + 1:]
        return ParentNode(f"h{heading_level}", text_to_children(stripped_block))

    if block_type == BlockType.CODE:
        actual_content = block[3:-3].strip()
        return ParentNode("pre", [LeafNode("code", actual_content)])

    if block_type == BlockType.QUOTE:
        stripped_quote = "\n".join(line[2:] if len(line) > 1 else "" for line in block.split("\n"))
        return ParentNode("blockquote", text_to_children(stripped_quote))

    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        items = [ParentNode("li", text_to_children(re.sub(r'^[-*+] ', '', line))) for line in lines]
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        items = [ParentNode("li", text_to_children(re.sub(r'^\d+\. ', '', line))) for line in lines]
        return ParentNode("ol", items)


def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_nodes.append(block_to_html(block))
    return ParentNode("div", block_nodes)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        current_block_type = block_to_block_type(block)
        if current_block_type == BlockType.HEADING and get_heading_level(block) == 1:
            return block[2:]
    raise ValueError("No title found: h1 block missing")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_content = markdown_to_html(markdown).to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)
