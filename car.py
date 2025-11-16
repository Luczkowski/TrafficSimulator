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
        self, road: Road, roads: List[Road], color: Tuple[int, int, int], speed: float = CAR_SPEED
    ):
        self.road = road
        self.roads = roads
        self.x, self.y = map(float, road.start)
        self.color = color
        self.speed = speed
        self.direction = random.choice(roads).name
        self.is_stopped = False

        dx = road.end[0] - road.start[0]
        dy = road.end[1] - road.start[1]
        length = math.hypot(dx, dy)
        self.vx = (dx / length) * speed if length != 0 else 0
        self.vy = (dy / length) * speed if length != 0 else 0

    def __str__(self) -> str:
        return f"Car {self.road.start} {self.road.end} {self.direction}"

    def is_car_ahead_in_range(self, cars: List[Car], distance: float) -> bool:
        """Check if there's a car ahead (in the direction of movement) within the given distance."""
        # Calculate position ahead of the car (in the direction of movement)
        ahead_x = self.x + self.vx * distance / self.speed if self.speed != 0 else self.x
        ahead_y = self.y + self.vy * distance / self.speed if self.speed != 0 else self.y
        
        for other in cars:
            if other is self:
                continue
            if other.road != self.road:
                continue
            # Check if other car is close to the "ahead" position
            dx = abs(other.x - ahead_x)
            dy = abs(other.y - ahead_y)
            if dx < CAR_SIZE + COLLISION_MARGIN and dy < CAR_SIZE + COLLISION_MARGIN and \
                other.is_stopped == True:
                return True
        return False
    
    def orientation(self, A, B, C) -> int:
        val = (B[1] - A[1]) * (C[0] - B[0]) - (B[0] - A[0]) * (C[1] - B[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2
        
    def if_cross(self, A, B, C, D) -> bool:
        o1 = self.orientation(A, B, C)
        o2 = self.orientation(A, B, D)
        o3 = self.orientation(C, D, A)
        o4 = self.orientation(C, D, B)

        if o1 != o2 and o3 != o4:
            return True
        return False
    
    def crossroad_point(self, A, B, C, D) -> Tuple[float, float]:
        a1 = B[1] - A[1]
        b1 = A[0] - B[0]
        c1 = a1 * A[0] + b1 * A[1]

        a2 = D[1] - C[1]
        b2 = C[0] - D[0]
        c2 = a2 * C[0] + b2 * C[1]

        det = a1 * b2 - a2 * b1
        if det == 0:
            return None
        
        Px = (b2 * c1 - b1 * c2) / det
        Py = (a1 * c2 - a2 * c1) / det
        return (Px, Py)
    
    def distance(self, A, P) -> float:
        return math.sqrt((P[0] - A[0])**2 + (P[1] - A[1])**2)

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
                self.is_stopped = True
                return False
            
        # Crossroad check
        # for road in self.roads:
        #     if road == self.road:
        #         continue
            # Ax, Ay = road.start[0], road.start[1]
            # Bx, By = road.end[0], road.end[1]
            # Cx, Cy = self.x, self.y
            # nominator = abs((Bx - Ax) * (Cy - Ay) - (By - Ay) * (Cx - Ax))
            # denominator = math.sqrt((By - Ay)**2 + (Bx - Ax)**2)
            # distance = nominator / denominator

            # to_car_x = Cx - Ax
            # to_car_y = Cy - Ay
            # dot_product = to_car_x * self.vx + to_car_y * self.vy

            # # If car is close to crossroad, check if there's a car ahead within 2 car sizes
            # if distance < CAR_SIZE + COLLISION_MARGIN and \
            #     dot_product > 0 and \
            #     self.is_car_ahead_in_range(cars, 2 * CAR_SIZE):
            #     self.is_stopped = True
            #     return False

            # if self.if_cross(road.start, road.end, (self.x, self.y), self.road.end):
            #     P = self.crossroad_point(road.start, road.end, (self.x, self.y), self.road.end)
            #     distance = self.distance((self.x, self.y), P)
            #     if P and distance < CAR_SIZE + COLLISION_MARGIN and \
            #         self.is_car_ahead_in_range(cars, 2 * CAR_SIZE):
            #         self.is_stopped = True
            #         return False
            

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
                    self.is_stopped = True
                    return False
        
        self.is_stopped = False
        return True

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            #(int(self.x + 1), int(self.y + 1), CAR_SIZE, CAR_SIZE),
            (self.x - CAR_SIZE / 2, self.y - CAR_SIZE / 2, CAR_SIZE, CAR_SIZE),
        )

    def has_reached_end(self) -> bool:
        dx = self.road.end[0] - self.x
        dy = self.road.end[1] - self.y
        return bool((dx * self.vx <= 0) and (dy * self.vy <= 0))

    def check_turn(self, roads: List[Road]) -> None:
        tolerance = 500

        # Check if car is on line between road start and end points
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
