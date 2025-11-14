import pygame

from configuration import *


class Light:
    x: int
    y: int
    direction: str
    automatic_control: bool

    def __init__(
        self, x: int, y: int, direction: str, automatic_control: bool = True
    ):
        self.x: int = x
        self.y: int = y
        self.direction: str = direction  # renamed from name to direction
        self.state: bool = True
        self.automatic_control: bool = automatic_control

    def check_state(self, directions: str | tuple[str, ...] | None) -> None:
        if directions is None:
            self.state = False
        elif isinstance(directions, str):
            self.state = self.direction == directions
        else:
            self.state = self.direction in directions

    def draw(self, surface: pygame.Surface) -> None:
        color = GREEN if self.state else RED
        pygame.draw.rect(surface, color, (self.x, self.y, 8, 8))

    def get_state(self) -> bool:
        return self.state

    def set_state(self, state: bool) -> None:
        self.state = state
