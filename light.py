import time, pygame

class Light:
    def __init__(self, x, y, time_true=2, time_false=2):
        self.x = x
        self.y = y
        self.state = True
        self.time_true = time_true
        self.time_false = time_false
        self.last_toggle_time = time.time()
        self.state_change_time = self.time_false

    def toggle_state(self):
        current_time = time.time()
        if current_time - self.last_toggle_time >= self.state_change_time:
            self.state = not self.state
            self.last_toggle_time = current_time
            self.state_change_time = self.time_true if self.state else self.time_false

    def draw(self, surface):
        color = (0, 255, 0) if self.state else (255, 0, 0)
        pygame.draw.rect(surface, color, (self.x, self.y, 5, 5))