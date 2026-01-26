import pyray as pr
import os

from components.component import Component

class GameList(Component):
    def __init__(self, x, y, width, height, props=None):
        super().__init__(x, y, width, height, props)
        self.games = []
        self.selected_index = 0
        
        # props
        self.font_size = self.props.get("font_size", 20)
        self.font_color = self.parse_color(self.props.get("font_color", "#FFFFFF"))
        self.selected_font_color = self.parse_color(self.props.get("selected_font_color", "#FFFF00"))
        
    
    def update(self):
        super().update()
    
    def draw(self): 
        super().draw()
        start_x = int(self.rect.x)
        start_y = int(self.rect.y)
                
        for i, game in enumerate(self.games):
                            
            color = self.selected_font_color if i == self.selected_index else self.font_color
            title = game[0]

            pr.draw_text(title, start_x, start_y + (i * 30), self.font_size, color)
            pr.draw_text(title, start_x, start_y + (i * 30), self.font_size, color)