import pyray as pr

class Component:
    def __init__(self, x, y, width, height, props=None, state=None):
        self.rect = pr.Rectangle(x, y, width, height)
        # defaults props to nothing
        self.props = props if props is not None else {}
        self.state = state
        
    def update(self):
        """Called on update loops"""
        
        pass
        
    def draw(self):
        """Called every frame"""
        
        pass

    def parse_color(self, color_val):
        if isinstance(color_val, str) and color_val.startswith("#"):
            hex_str = color_val.lstrip("#")
            if len(hex_str) == 6:
                hex_str += "FF"
            try:
                return pr.get_color(int(hex_str, 16))
            except ValueError:
                # Return a fallback color (Magenta) to indicate error, rather than crashing
                return pr.MAGENTA
        return color_val