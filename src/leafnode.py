from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError()
        if self.tag == "" or self.tag == None:
            return self.value
        props = self.props_to_html()
        if len(props) != 0:
            props = " " + props

        return f'<{self.tag}{props}>{self.value}</{self.tag}>'