import math
import random
import time
from typing import List, Optional, Tuple

import pygame

from car import Car
from configuration import *
from light import Light


class Road:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        name: str,
        color: Tuple[int, int, int],
        spawn_rate: float = 1.0,
    ) -> None:
        self.start = start
        self.end = end
        self.name = name
        self.color = color

        # Mean spawn rate (cars per second)
        self.spawn_rate = spawn_rate
        self.default_spawn_rate: float = spawn_rate

        # Time-based spawning variables
        self.time_since_last_spawn = 0.0
        if self.spawn_rate > 0:
            self.next_spawn_interval = random.expovariate(self.spawn_rate)
        else:
            self.next_spawn_interval = math.inf

        self.last_update_time = time.time()

    def set_spawn_rate(self, rate: float) -> None:
        self.spawn_rate = rate

        if self.spawn_rate > 0:
            self.next_spawn_interval = random.expovariate(self.spawn_rate)
        else:
            self.next_spawn_interval = math.inf

    def spawn_car(
        self,
        cars: List["Car"],
        stops: List["Light"],
        roads: List["Road"],
        dt: float,
        speed: float = CAR_SPEED,
    ) -> None:

        # Accumulate elapsed time (seconds)
        self.time_since_last_spawn += dt

        # Check if it's time to spawn a new car
        if self.time_since_last_spawn >= self.next_spawn_interval:
            car = Car(self, roads=roads, color=self.color, speed=speed)

            # Only add if it can safely move
            if car.can_move(cars, stops):
                cars.append(car)

            # Reset timer and draw new random waiting time
            self.time_since_last_spawn = 0.0
            if self.spawn_rate > 0:
                self.next_spawn_interval = random.expovariate(self.spawn_rate)
            else:
                self.next_spawn_interval = math.inf

    def draw(self, surface: pygame.Surface) -> None:
        # Offset lines by half of CAR_SIZE on both sides of the road center
        half_offset = int(round(CAR_SIZE / 2))

        if self.start[1] == self.end[1]:
            # horizontal road
            y_center = self.start[1]
            y1 = y_center - half_offset -1
            y2 = y_center + half_offset
            pygame.draw.line(surface, WHITE, (self.start[0], y1), (self.end[0], y1))
            pygame.draw.line(surface, WHITE, (self.start[0], y2), (self.end[0], y2))
        elif self.start[0] == self.end[0]:
            # vertical road
            x_center = self.start[0]
            x1 = x_center - half_offset - 1
            x2 = x_center + half_offset
            pygame.draw.line(surface, WHITE, (x1, self.start[1]), (x1, self.end[1]))
            pygame.draw.line(surface, WHITE, (x2, self.start[1]), (x2, self.end[1]))
        else:
            # fallback: draw center line for non-axis-aligned roads
            pygame.draw.line(surface, WHITE, self.start, self.end)
