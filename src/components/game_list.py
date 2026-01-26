import pyray as pr
from components.component import Component

class GameList(Component):
    def __init__(self, x, y, width, height, props=None, state=None):
        super().__init__(x, y, width, height, props, state)
        
        # props
        self.font_size = self.props.get("font_size", 20)
        self.font_color = self.parse_color(self.props.get("font_color", "#FFFFFF"))
        self.selected_font_color = self.parse_color(self.props.get("selected_font_color", "#FFFF00"))
        
        self.pressed = 0
    
    def handle_input(self, input_manager):
        super().handle_input(input_manager)

        if input_manager.is_pressed("UP"):
            self.state.selected_index = (self.state.selected_index - 1) % len(self.state.games)            
        elif input_manager.is_pressed("DOWN"):
            self.state.selected_index = (self.state.selected_index + 1) % len(self.state.games)
           

    def update(self):
        super().update()
        if not self.state or not self.state.games:
            return       


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