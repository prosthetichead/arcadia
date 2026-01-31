import pyray as pr
from frontend.components.component import Component

class PlaylistList(Component):
    def __init__(self, x, y, width, height, props=None, state=None):
        super().__init__(x, y, width, height, props, state)
        
        # props
        self.font_size = self.props.get("font_size", 20)
        self.font_color = self.parse_color(self.props.get("font_color", "#FFFFFF"))
        self.selected_font_color = self.parse_color(self.props.get("selected_font_color", "#FFFF00"))
        self.text_align = self.props.get("text_align", "center")
        
        self.border_thickness = self.props.get("border_thickness", 2)       
        self.border_color = self.parse_color(self.props.get("border_color", "#FF0000"))
    
    def handle_input(self, input_manager):
        super().handle_input(input_manager)

    def update(self):
        super().update()
        if not self.state or not self.state.playlists:
            return       

    def draw(self): 
        super().draw()
        if not self.state:
            return
        
    