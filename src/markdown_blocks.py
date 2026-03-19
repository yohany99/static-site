from enum import Enum
from textnode import TextNode, TextType, text_to_textnodes, text_node_to_html_node
from parentnode import ParentNode
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if re.match(r"^```", lines[0]) and re.match(r"^```", lines[-1]) and len(lines) > 1:
        return BlockType.CODE
    if all(re.match(r"^>", line) for line in lines):
        return BlockType.QUOTE
    if all(re.match(r"^- ", line) for line in lines):
        return BlockType.ULIST
    if all(re.match(rf"^{i+1}\. ", line) for i, line in enumerate(lines)):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        child_node = block_to_html_node(block)
        children.append(child_node)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    block = block[level + 1:]
    lines = block.split("\n")
    heading = " ".join(lines)
    children = text_to_children(heading)
    tag = "h" + str(level)
    return ParentNode(tag, children)

def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line = line[2:]
        children.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", children)

def olist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line = line[3:]
        children.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ol", children)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children


        
