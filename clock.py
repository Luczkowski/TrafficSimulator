import time, datetime

class LightClock:
    def __init__(self, sequence, pause_duration=1):
        self.sequence = []
        self.current_directions=[]
        for letter, duration in sequence:
            self.sequence.append((letter, duration))
            self.sequence.append((None, pause_duration))

        self.current_index = 0
        self.current_directions, self.duration = self.sequence[0]
        self.elapsed = 0.0

    def update(self, dt):
        self.elapsed += dt

        if self.elapsed >= self.duration:
            self.current_index = (self.current_index + 1) % len(self.sequence)
            self.current_directions, self.duration = self.sequence[self.current_index]
            self.elapsed = 0.0
    
    def get_current_directions(self):
        return self.current_directions
