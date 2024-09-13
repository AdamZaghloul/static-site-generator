import re

from htmlnode import *
from leafnode import *
from textnode import *
from parentnode import *

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
            return LeafNode("img", "", {"src":text_node.url,"alt":text_node.text})
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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []

    for block in blocks:
        if block != "":
            final_blocks.append(block.strip(" \n"))
    
    return final_blocks

def block_to_block_type(text):
    prefix = text.split(" ")

    if text[0] == "#" or text[0:2] == "##" or text[0:3] == "###" or text[0:4] == "####" or text[0:5] == "#####" or text[0:6] == "######":
        return "heading"
    if text[0:3] == "```" and text[-3:] == "```":
        return "code"
    
    ul = True
    ol = True
    quote = True
    count = 1

    lines = text.split("\n")

    for line in lines:
        if line[0] != ">":
            quote = False
        if line[0:2] != "* " and line[0:2] != "- ":
            ul = False
        if ol == True:
            num = line.split(". ", 1)
            if num[0].isnumeric(): 
                if int(num[0]) != count:
                    ol = False
            else:
                ol = False

        count += 1
        
    if quote == True:
        return "quote"
    if ul == True:
        return "unordered_list"
    if ol == True:
        return "ordered_list"
    
    return "paragraph"

def markdown_to_html_node(markdown):
    str_blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in str_blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case "heading":
                html_nodes.append(markdown_to_html_node_heading(block))
            case "code":
                html_nodes.append(markdown_to_html_node_code(block))
            case "quote":
                html_nodes.append(markdown_to_html_node_quote(block))
            case "unordered_list":
                html_nodes.append(markdown_to_html_node_list("u", block))
            case "ordered_list":
                html_nodes.append(markdown_to_html_node_list("o", block))
            case "paragraph":
                html_nodes.append(markdown_to_html_node_paragraph(block))
            case _:
                raise Exception("Invalid Block Type")
    
    return ParentNode("div", html_nodes, None)
    
def markdown_to_html_node_heading(markdown):
    count = 0

    for char in markdown:
        if char == "#":
            count += 1
        else:
            break
    
    text = markdown[count:].strip()

    children = text_to_children(text)

    return ParentNode(f"h{count}", children, None)

def markdown_to_html_node_code(markdown):
    text = markdown[3:-3].strip()

    children = text_to_children(text)

    code_node = ParentNode("code", children, None)
    pre_node = ParentNode("pre", [code_node], None)

    return pre_node

def markdown_to_html_node_quote(markdown):
    lines = markdown.split("\n")
    new_lines = []

    for line in lines:
        line = line[1:]
        new_lines.append(line)
    
    children = text_to_children("\n".join(new_lines).strip())
    
    return ParentNode("blockquote", children, None)

def markdown_to_html_node_list(list_type, markdown):

    lines = markdown.split("\n")
    items = []
    count = 1

    if list_type == "o":
        tag = "ol"
    elif list_type == "u":
        tag = "ul"
    else:
        raise Exception("Invalid List Type")

    for line in lines:
        if list_type == "o":
            line = line.split(f"{count}. ")[1]
            count += 1
        elif list_type == "u":
            line = line[2:] 
        
        items.append(ParentNode("li", text_to_children(line), None))
    
    return ParentNode(tag, items, None)

def markdown_to_html_node_paragraph(markdown):
    
    return ParentNode("p", text_to_children(markdown), None)

def text_to_children(text):
    children = []

    text_nodes = text_to_textnodes(text)

    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    
    return children

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line[0] == "#" and line[1] != "#":
            return line[1:].strip()
    
    raise Exception("No h1 header in markdown")