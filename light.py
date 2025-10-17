import time
import pygame
from configuration import *

class Light:
    def __init__(self, x, y, phases=None, automatic_control=True):
        self.x = x
        self.y = y
        self.phases = phases if phases else [(2, True), (2, False)]
        self.current_phase = 0
        self.state = self.phases[0][1]
        self.last_toggle_time = time.time()
        self.automatic_control = automatic_control

    def toggle_state(self):
        if self.automatic_control:
            current_time = time.time()
            phase_duration, _ = self.phases[self.current_phase]
            if current_time - self.last_toggle_time >= phase_duration:
                self.current_phase = (self.current_phase + 1) % len(self.phases)
                self.state = self.phases[self.current_phase][1]
                self.last_toggle_time = current_time

    def draw(self, surface):
        color = GREEN if self.state else RED
        pygame.draw.rect(surface, color, (self.x, self.y, 8, 8))