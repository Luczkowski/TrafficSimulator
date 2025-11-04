import time
import pygame
from configuration import *


class Light:
    def __init__(self, x, y, name, automatic_control=True):
        self.x = x
        self.y = y
        self.name = name
        self.state = True
        self.automatic_control = automatic_control

    def check_state(self, current_directions):
        if current_directions is not None: 
            self.state = self.name in current_directions
        else:
            self.state = False

    def draw(self, surface):
        color = GREEN if self.state else RED
        pygame.draw.rect(surface, color, (self.x, self.y, 8, 8))

    def get_state(self):
        return self.state
    
    def set_state(self, state: bool):
        self.state = state
