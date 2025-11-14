from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, List, Tuple

import pygame

from configuration import *
from light import Light

if TYPE_CHECKING:
    from road import Road


class Car:
    def __init__(
        self, road: Road, color: Tuple[int, int, int], speed: float = CAR_SPEED
    ):
        self.road = road
        self.x, self.y = map(float, road.start)
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
        future_x = self.x + self.vx
        future_y = self.y + self.vy

        # Collision check with other cars
        for other in cars:
            if other is self:
                continue
            dx = abs(other.x - future_x)
            dy = abs(other.y - future_y)
            if (
                dx < CAR_SIZE + COLLISION_MARGIN
                and dy < CAR_SIZE + COLLISION_MARGIN
            ):
                return False

        # Stoplight check
        for stop in stops:
            if stop.direction not in self.road.name:
                continue

            # If already on the stop — ignore this light
            if (
                abs(stop.x - self.x) < CAR_SIZE
                and abs(stop.y - self.y) < CAR_SIZE
            ):
                continue

            # If light is red and car is about to cross it — stop
            if not stop.state:
                if (
                    abs(stop.x - future_x) < CAR_SIZE
                    and abs(stop.y - future_y) < CAR_SIZE
                ):
                    return False

        return True

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            (int(self.x + 1), int(self.y + 1), CAR_SIZE, CAR_SIZE),
        )

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
                if test < tolerance and self.direction == road.name:
                    self.road = road
                    self.direction = ""
                    self.x, self.y = x3, y3

                    dx = road.end[0] - road.start[0]
                    dy = road.end[1] - road.start[1]
                    length = math.hypot(dx, dy)
                    self.vx = (dx / length) * self.speed if length != 0 else 0
                    self.vy = (dy / length) * self.speed if length != 0 else 0

    def update(
        self, cars: List[Car], roads: List[Road], stops: List[Light]
    ) -> None:
        self.check_turn(roads)
        if self.can_move(cars, stops):
            self.move()
        if self.has_reached_end():
            cars.remove(self)
