from enum import Enum
import re
import os
from htmlnode import ParentNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph" 
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """Next level up to figure out splitting a page of text, header etc into blocks"""
    new_blocks = []
    blocks = markdown.split("\n\n")
    for i, block in enumerate(blocks):
        new_block = block.strip()
        if new_block != "":
            new_blocks.append(new_block)
    return new_blocks

def block_to_block_type(block):
    """Get the block type for the blocks"""
    get_lines = block.split("\n")
    first_line = get_lines[0]
    last_line = get_lines[-1]
    if len(first_line) >=7:
        if first_line[0] == "#":
            count = 0
            for c in first_line:
                if c == "#":
                    count += 1
                else:
                    break
            if 1 <= count <= 6 and first_line[count] == " ":
                return BlockType.HEADING
    if first_line.startswith("```") and last_line.endswith("```"):
            return BlockType.CODE
    if all(line.startswith(">") for line in get_lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in get_lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i+1}. ") for i, line in enumerate(get_lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    """For getting the leaf nodes for everything but code blocks"""
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def remove_block_markdown_quotes_and_list(text):
    """for taking out the markdown info from quotes and lists on valid blocks"""
    get_lines = text.split("\n")
    new_lines = []
    for line in get_lines:
        match = re.match(r"\d+\.\s+", line)
        if match:
            new_line = line[match.end():]
        else:
            new_line = line[1:]
            new_line = new_line.strip()
        new_lines.append(new_line)
    return new_lines


def markdown_to_html_node(markdown):
    """Brining everything together in going from markdown to html"""
    blocks = markdown_to_blocks(markdown)
    parents = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            content = block.replace("\n", " ")
            children = text_to_children(content)
            parents.append(ParentNode("p", children))
        elif block_type == BlockType.HEADING:
            count = 0
            for c in block:
                if c == "#":
                    count += 1
                else:
                    break
            content = block[count+1:]
            children = text_to_children(content)
            parents.append(ParentNode(f"h{count}", children))
        elif block_type == BlockType.CODE:
            get_lines = block.split("\n")
            first_line = get_lines[0]
            last_line = get_lines[-1]
            if first_line == "```" and last_line == "```":
                content ="\n".join(get_lines[1:-1]) + "\n"  
            else:
                content = block[3:]
                content = content[:-3]
            if not content.endswith("\n"):
                content = content + "\n"
            if content:
                child = LeafNode(None, content)
                parents.append(ParentNode("pre", [ParentNode("code", [child])]))
        elif block_type == BlockType.QUOTE:
            new_lines = remove_block_markdown_quotes_and_list(block)
            content = " ".join(new_lines)
            children = text_to_children(content)
            parents.append(ParentNode("blockquote", children))
        elif block_type == BlockType.UNORDERED_LIST:
            new_lines = remove_block_markdown_quotes_and_list(block)
            children = []
            for line in new_lines:
                child = text_to_children(line)
                children.append(ParentNode("li", child))
            parents.append(ParentNode("ul", children))
        elif block_type == BlockType.ORDERED_LIST:
            new_lines = remove_block_markdown_quotes_and_list(block)
            children = []
            for line in new_lines:
                child = text_to_children(line)
                children.append(ParentNode("li", child))
            parents.append(ParentNode("ol", children)) 
    return ParentNode("div", parents)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            content = block[2:]
            return content.strip()
    raise Exception("There must be a main title starting with # ")

def generate_page(from_path, template_path, dest_path, basepath):
    if os.path.exists(from_path):
        if os.path.exists(template_path):
            print(f"Generating page from {from_path} to {dest_path} using {template_path}")
            with open(from_path) as s:
                source_markdown = s.read()
            with open(template_path) as t:
                template = t.read()
            almost_html = markdown_to_html_node(source_markdown)
            source_as_html = almost_html.to_html()
            title = extract_title(source_markdown)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", source_as_html)
            template = template.replace('href="/', f'href="{basepath}')
            full_html_page = template.replace('src="/', f'src="{basepath}')
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as w:
                w.write(full_html_page)
        else:
            raise Exception(f"{template_path} does not exist.")
    else:
        raise Exception(f"{from_path} does not exist.")


