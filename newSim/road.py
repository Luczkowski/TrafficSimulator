import pygame

from configuration import *
from carTest import Car

class Road:
    def __init__(self, start, end, stop, name, color, directions=[], spawn_frequency=60):
        self.start = start
        self.end = end
        self.stop = stop
        self.name = name
        self.color = color
        self.directions = list(directions)
        self.directions.append(name)
        self.spawn_frequency = spawn_frequency
        self.spawn_timer = 0

    def __str__(self):
        return f"Road {self.name} with directions {self.directions}"

    def draw(self, surface):
        pygame.draw.line(surface, WHITE, self.start, self.end)
        pygame.draw.circle(surface, RED, (self.stop[0], self.stop[1]), 5)
        if self.start[1] == self.end[1]:
            pygame.draw.line(surface, WHITE, (self.start[0], self.start[1] + CAR_SIZE), (self.end[0], self.end[1] + CAR_SIZE))
        if self.start[0] == self.end[0]:
            pygame.draw.line(surface, WHITE, (self.start[0] + CAR_SIZE, self.start[1]), (self.end[0] + CAR_SIZE, self.end[1]))

    def set_spawn_frequency(self, frequency):
        self.spawn_frequency = frequency

    def spawn_car(self, cars, speed=2):
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_frequency:
            car = Car(self, color=self.color, speed=speed)
            if car.can_move(cars):
                cars.append(car)
            self.spawn_timer = 0
