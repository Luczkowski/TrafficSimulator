from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, List, Tuple

import pygame

if TYPE_CHECKING:
    from road import Road

from configuration import *
from light import Light


class Car:
    def __init__(self, road: Road, color: Tuple[int, int, int], speed: int = CAR_SPEED):
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

    def __str__(self) -> str:
        return f"Car {self.road.start} {self.road.end} {self.direction}"

    def can_move(self, cars: List[Car], stops: List[Light]) -> bool:
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
            if my_future_rect.colliderect(stop_rect) and stop.state is False:
                return False
        return True

    def move(self) -> None:
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), 20, 20))

    def has_reached_end(self) -> bool:
        dx = self.road.end[0] - self.x
        dy = self.road.end[1] - self.y
        return bool((dx * self.vx <= 0) and (dy * self.vy <= 0))

    def check_turn(self, roads: List[Road]) -> None:
        tolerance = 500
        for road in roads:
            if road != self.road:
                x1, y1 = road.start[0], road.start[1]
                x2, y2 = road.end[0], road.end[1]
                x3, y3 = self.x, self.y

                test = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))

                # if test < tolerance and self.direction == road.name:
                #     self.__init__(road, color=self.color)
                #     self.direction = ""
                #     self.x, self.y = x3, y3

                if test < tolerance and self.direction == road.name:
                    self.road = road
                    self.direction = ""
                    self.x, self.y = x3, y3

                    dx = road.end[0] - road.start[0]
                    dy = road.end[1] - road.start[1]
                    length = math.hypot(dx, dy)
                    self.vx = (dx / length) * self.speed if length != 0 else 0
                    self.vy = (dy / length) * self.speed if length != 0 else 0

    def update(self, cars: List[Car], roads: List[Road], stops: List[Light]) -> None:
        self.check_turn(roads)
        if self.can_move(cars, stops):
            self.move()
        if self.has_reached_end():
            cars.remove(self)
