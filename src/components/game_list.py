import pyray as pr
from components.component import Component

class GameList(Component):
    def __init__(self, x, y, width, height, props=None, state=None):
        super().__init__(x, y, width, height, props, state)
        
        # props
        self.font_size = self.props.get("font_size", 20)
        self.font_color = self.parse_color(self.props.get("font_color", "#FFFFFF"))
        self.selected_font_color = self.parse_color(self.props.get("selected_font_color", "#FFFF00"))
        
    
    def update(self):
        super().update()
        if not self.state or not self.state.games:
            return

        # Handle navigation - this updates the shared state
        if pr.is_key_pressed(pr.KEY_DOWN):
            self.state.selected_index = (self.state.selected_index + 1) % len(self.state.games)
        elif pr.is_key_pressed(pr.KEY_UP):
            self.state.selected_index = (self.state.selected_index - 1) % len(self.state.games)
    
    def draw(self): 
        super().draw()
        if not self.state:
            return

        start_x = int(self.rect.x)
        start_y = int(self.rect.y)
                
        for i, game in enumerate(self.state.games):
                            
            color = self.selected_font_color if i == self.state.selected_index else self.font_color
            title = game[0]

            pr.draw_text(title, start_x, start_y + (i * 30), self.font_size, color)
            pr.draw_text(title, start_x, start_y + (i * 30), self.font_size, color)