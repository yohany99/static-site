from enum import Enum
from leafnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            split_text = node.text.split(delimiter)
            new_node = []
            if len(split_text) % 2 == 0:
                raise Exception("matching closing delimiter not found")
            else:
                for i, e in enumerate(split_text):
                    if len(e) == 0:
                        continue
                    elif i % 2 == 0:
                        new_node.append(TextNode(e, TextType.TEXT))
                    else:
                        new_node.append(TextNode(e, text_type))
            new_nodes.extend(new_node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        extract_list = extract_markdown_images(text)
        if not extract_list:
            if len(text) > 0:
                new_nodes.append(node)
        else:
            for alt, url in extract_list:
                sections = text.split(f"![{alt}]({url})", 1)
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text = sections[1]
            if len(text):
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        extract_list = extract_markdown_links(text)
        if not extract_list:
            if len(text) > 0:
                new_nodes.append(node)
        else:
            for alt, url in extract_list:
                sections = text.split(f"[{alt}]({url})", 1)
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK, url))
                text = sections[1]
            if len(text):
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = {
        "**" : TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }
    for key in delimiters:
        nodes = split_nodes_delimiter(nodes, key, delimiters[key])
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)


