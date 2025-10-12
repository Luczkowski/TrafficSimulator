import pygame, math, random
from configuration import *

class Car:
    def __init__(self, road, color, speed=CAR_SPEED):
        self.road = road
        self.x, self.y = road.start
        self.color = color
        self.speed = speed
        self.direction = random.choice(self.road.directions)

        dx = road.end[0] - road.start[0]
        dy = road.end[1] - road.start[1]
        length = math.hypot(dx, dy)
        self.vx = (dx / length) * speed if length != 0 else 0
        self.vy = (dy / length) * speed if length != 0 else 0

    def __str__(self):
        return f"Car {self.road.start} {self.road.end} {self.direction}"

    def can_move(self, cars, stops):
        my_rect = pygame.Rect(self.x, self.y, 20, 20)
        my_future_rect = pygame.Rect(self.x + self.vx - 2, self.y + self.vy - 2, 24, 24)
        for other in cars:
            if other is self:
                continue
            other_rect = pygame.Rect(other.x, other.y, 20, 20)
            if my_future_rect.colliderect(other_rect):
                return False

        for stop in stops:
            stop_rect = pygame.Rect(stop.x, stop.y, 1, 1)
            if my_rect.colliderect(stop_rect):
                return True
            if my_future_rect.colliderect(stop_rect) and stop.state == False:
                return False
        return True

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), 20, 20))

    def has_reached_end(self):
        dx = self.road.end[0] - self.x
        dy = self.road.end[1] - self.y
        return (dx * self.vx <= 0) and (dy * self.vy <= 0)

    def check_turn(self, roads):
        tolrance=500
        for road in roads:
            if road != self.road:
                x1, y1 = road.start[0], road.start[1]
                x2, y2 = road.end[0], road.end[1]
                x3, y3 = self.x, self.y

                test = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))

                if test < tolrance and self.direction == road.name:
                    self.__init__(road, color=self.color)
                    self.direction = None
                    self.x, self.y = x3, y3

    def update(self, cars, roads, stops):
        self.check_turn(roads)
        if self.can_move(cars, stops):
            self.move()
        if self.has_reached_end():
            cars.remove(self)