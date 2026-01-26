import pyray as pr
from components.component import Component

class GameList(Component):
    def __init__(self, x, y, width, height, props=None, state=None):
        super().__init__(x, y, width, height, props, state)
        
        # props
        self.font_size = self.props.get("font_size", 20)
        self.font_color = self.parse_color(self.props.get("font_color", "#FFFFFF"))
        self.selected_font_color = self.parse_color(self.props.get("selected_font_color", "#FFFF00"))
        self.text_align = self.props.get("text_align", "center")
        
        self.pressed = 0
    
    def handle_input(self, input_manager):
        super().handle_input(input_manager)
                   

    def update(self):
        super().update()
        if not self.state or not self.state.games:
            return       


    def draw(self): 
        super().draw()
        if not self.state or not self.state.games:
            return

        center_y = self.rect.y + (self.rect.height / 2)
        item_height = int(self.font_size * 1.5)
        visible_count = int(self.rect.height / item_height) // 2 + 2
        num_games = len(self.state.games)

        pr.draw_rectangle_lines_ex(self.rect, 2, self.font_color)
        
        pr.begin_scissor_mode(int(self.rect.x), int(self.rect.y), int(self.rect.width), int(self.rect.height))
        for i in range(-visible_count, visible_count + 1):
            index = (self.state.selected_index + i) % num_games
            game = self.state.games[index]
            title = game[0]
            y_pos = int(center_y + (i * item_height) - (self.font_size / 2))
            
            text_width = pr.measure_text(title, self.font_size)
            
            if self.text_align == "left":
                text_x = int(self.rect.x + 10)
            elif self.text_align == "right":
                text_x = int(self.rect.x + self.rect.width - text_width - 10)
            else:
                text_x = int(self.rect.x + (self.rect.width - text_width) / 2)
            
            color = self.selected_font_color if i == 0 else self.font_color
            pr.draw_text(title, text_x, y_pos, self.font_size, color)
        pr.end_scissor_mode()