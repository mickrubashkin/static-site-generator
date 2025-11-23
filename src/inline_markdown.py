from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"INVALID MARKDOWN: matching closing delimeter ({delimiter}) not found")

        new_parts = []

        for i in range(len(parts)):
            if len(parts[i]) == 0:
                continue
            node_type = TextType.TEXT if i % 2 == 0 else text_type
            new_parts.append(TextNode(parts[i], node_type))

        new_nodes.extend(new_parts)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
