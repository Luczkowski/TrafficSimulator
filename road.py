from typing import List, Tuple

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
        directions: List[str] | None = None,
        spawn_frequency: int = 60,
    ):
        self.start = start
        self.end = end
        self.name = name
        self.color = color

        self.directions = list(directions) if directions is not None else []

        # to jest automatyczne dodawanie domyślnego kierunku drogi do możliwych celów
        # jeśli to wyłączymy, to domyślny kierunek drogi musi być uwzględniony przy tworzeniu drogi
        # self.directions.append(name)

        self.spawn_frequency = spawn_frequency
        self.spawn_timer = 0

    def __str__(self) -> str:
        return f"Road {self.name} with directions {self.directions}"

    def draw(self, surface: pygame.Surface) -> None:
        # draw first line
        pygame.draw.line(surface, WHITE, self.start, self.end)

        # second line - horizontal roads
        if self.start[1] == self.end[1]:
            pygame.draw.line(
                surface,
                WHITE,
                (self.start[0], self.start[1] + CAR_SIZE),
                (self.end[0], self.end[1] + CAR_SIZE),
            )

        # second line - vertical roads
        elif self.start[0] == self.end[0]:
            pygame.draw.line(
                surface,
                WHITE,
                (self.start[0] + CAR_SIZE, self.start[1]),
                (self.end[0] + CAR_SIZE, self.end[1]),
            )

        # TODO add diagonal roads

    def set_spawn_frequency(self, frequency: int) -> None:
        self.spawn_frequency = frequency

    def spawn_car(self, cars: List["Car"], stops: List["Light"], speed: int = 2) -> None:
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_frequency:
            car = Car(self, color=self.color, speed=speed)
            if car.can_move(cars, stops):
                cars.append(car)
            self.spawn_timer = 0
