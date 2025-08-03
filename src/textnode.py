import re
from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
            
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

    
def text_node_to_html_node(text_node):
    """get the delimter and text type"""
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": f'{text_node.url}'})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": f'{text_node.url}', "alt": f'{text_node.text}'})
    else:
        raise Exception("No text type, that is required")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split the node with a known texttype"""
    new_nodes = []
    if old_nodes:
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception(f"Missing closing {delimiter}")
            for i, part in enumerate(split_nodes):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        return new_nodes

def extract_markdown_images(text):
    """Get the image info from Text"""
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    """Get url info from text"""
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    """split text into nodes and image ones"""
    new_nodes = []
    if old_nodes:
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            text = node.text
            matches = extract_markdown_images(text)
            if matches:
                for image_alt, image_link in matches:
                    parts = text.split(f"![{image_alt}]({image_link})", 1)
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                    text = parts[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
                    
def split_nodes_link(old_nodes):
    """Split the text into nodes and links types nodes"""
    new_nodes = []
    if old_nodes:
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            text = node.text
            matches = extract_markdown_links(text)
            if matches:
                for alt, link_url in matches:
                    parts = text.split(f"[{alt}]({link_url})", 1)
                    if parts[0] != "":
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.LINK, link_url))
                    text = parts[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
                    

def text_to_textnodes(text):
    """bringing all the splits together"""
    node = TextNode(text, TextType.TEXT)
    new_nodes = [node]
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    #bold
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    #italic
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    #code
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes
                    
                    






    
