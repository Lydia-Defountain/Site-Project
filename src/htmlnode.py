
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html = ""
        if self.props:
            for key in self.props:
                html += f' {key}="{self.props[key]}"'
        return html

            
    def __repr__(self):
        return f"HTMLNode(Tag={self.tag!r}, Value={self.value!r}, Children={len(self.children)}, Props={self.props!r}"
    

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return f"{self.value}"
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        

