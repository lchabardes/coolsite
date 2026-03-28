


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        content = ""
        for key, val in self.props.items():
            content += f' {key}="{val}"'
        return content

    def __repr__(self):
        return(f"Tag:{self.tag}, value:{self.value}, children:{self.children}, properties:{self.props_to_html()}")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node should have a value")
        if self.tag is None:
            return self.value
        return(f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")
    
    def __repr__(self):
        return(f"Tag:{self.tag}, value:{self.value}, properties:{self.props_to_html()}")
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode should have a tag")
        if self.children is None:
            raise ValueError("ParentNode should have a children node")
        tag_start = f"<{self.tag}{self.props_to_html()}>"
        middle = ""
        for child in self.children:
            middle += child.to_html()
        tag_end = f"</{self.tag}>"
        return(tag_start + middle + tag_end)