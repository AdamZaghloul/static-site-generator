from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError()
        if len(self.children) == 0 or self.children == None:
            raise ValueError("No Children for Parent Node")
        props = self.props_to_html()
        if len(props) != 0:
            props = " " + props

        child_html = ""

        for child in self.children:
            
            child_html += child.to_html()

        return f'<{self.tag}{props}>{child_html}</{self.tag}>'