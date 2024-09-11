import re

from htmlnode import *
from leafnode import *
from textnode import *

def text_node_to_html_node(text_node):

    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case "image":
            return LeafNode("img", None, {"src":text_node.url,"alt":text_node.text})
        case _:
            return Exception("Invalid Text Node Type for Conversion")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != "text" or delimiter not in old_node.text:
            new_nodes.append(old_node)
        else:
            del_count = 0
            last_del = 0
            next_del = old_node.text.find(delimiter)

            while next_del != len(old_node.text):
                del_count += 1

                if del_count % 2 != 0:
                    new_nodes.append(TextNode(old_node.text[last_del:next_del], "text"))
                else:
                    new_nodes.append(TextNode(old_node.text[last_del:next_del], text_type))

                last_del = next_del+len(delimiter)
                next_del = old_node.text.find(delimiter, last_del)

                if next_del == -1:
                    next_del = len(old_node.text)
                
            if del_count % 2 == 0:
                new_nodes.append(TextNode(old_node.text[last_del:next_del], "text"))
            else:
                new_nodes.append(TextNode(old_node.text[last_del:next_del], text_type))    
            
            if del_count % 2 != 0:
                raise Exception("Invalid Markdown syntax")
                
    return new_nodes

def split_nodes_image(old_nodes):
    output = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            output.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            working_string = old_node.text
            for image in images:
                split = working_string.split(f"![{image[0]}]({image[1]})", 1)
                before = split[0]
                if len(split) > 1:
                    working_string = split[1]
                else:
                    working_string = ''

                if before != '':
                    output.append(TextNode(before, "text"))
                output.append(TextNode(image[0], "image", image[1]))
            
            if working_string != '':
                output.append(TextNode(working_string, "text"))
    
    return output

def split_nodes_link(old_nodes):
    output = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            output.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            working_string = old_node.text
            for link in links:
                split = working_string.split(f"[{link[0]}]({link[1]})", 1)
                before = split[0]
                if len(split) > 1:
                    working_string = split[1]
                else:
                    working_string = ''

                if before != '':
                    output.append(TextNode(before, "text"))
                output.append(TextNode(link[0], "link", link[1]))
            
            if working_string != '':
                output.append(TextNode(working_string, "text"))
    
    return output

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def text_to_textnodes(text):

    bold = split_nodes_delimiter([TextNode(text, "text")], "**", "bold")
    italic = split_nodes_delimiter(bold, "*", "italic")
    code = split_nodes_delimiter(italic, "`", "code")
    link = split_nodes_link(code)
    image = split_nodes_image(link)

    return image