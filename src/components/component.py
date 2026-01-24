import pyray as pr

class Component:
    def __init__(self, x, y, width, height, props=None):
        self.rect = pr.Rectangle(x, y, width, height)
        # defaults props to nothing
        self.props = props if props is not None else {}
        
    def update(self):
        """Called on update loops"""

        pass
        
    def draw(self):
        """Called every frame"""
        
        pass