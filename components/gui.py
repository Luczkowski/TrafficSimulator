import pygame

from typing import Tuple, Callable

from car import Car

from configuration import *


# Buttons
class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        color: Tuple[int, int, int],
        hover_color: Tuple[int, int, int],
        action: Callable[[], None] | None = None,
        font_size: int = 24,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


class StopButton(Button):
    def __init__(
        self,
        get_simulation_state: Callable[[], bool],
        set_simulation_state: Callable[[bool], None],
    ) -> None:
        super().__init__(
            20,
            WINDOW_HEIGHT - 70,
            120,
            40,
            "Stop",
            (180, 180, 180),
            (200, 200, 200),
            action=None,
        )
        self.get_simulation_state = get_simulation_state
        self.set_simulation_state = set_simulation_state

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                new_state = not self.get_simulation_state()
                self.set_simulation_state(new_state)

                self.text = "Stop" if new_state else "Start"


class RestartButton(Button):
    def __init__(self, set_cars: Callable[[list[Car]], None]) -> None:
        super().__init__(
            160,
            WINDOW_HEIGHT - 70,
            120,
            40,
            "Reset",
            (180, 180, 180),
            (200, 200, 200),
            action=None,
        )
        self.set_cars = set_cars

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.set_cars([])


class ToggleAutomaticControlButton(Button):
    def __init__(
        self,
        get_automatic_control: Callable[[], bool],
        set_automatic_control: Callable[[bool], None],
    ) -> None:
        super().__init__(
            WINDOW_WIDTH - 200,
            WINDOW_HEIGHT - 70,
            160,
            40,
            "Automatic mode",
            (180, 180, 180),
            (200, 200, 200),
            action=None,
        )
        self.get_automatic_control = get_automatic_control
        self.set_automatic_control = set_automatic_control

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.set_automatic_control(not self.get_automatic_control())
                if self.get_automatic_control() == True:
                    self.text = "Automatic mode"
                else:
                    self.text = "Manual mode"


class ToggleButton(Button):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text_on: str = "On",
        text_off: str = "Off",
        color: Tuple[int, int, int] = (180, 180, 180),
        hover_color: Tuple[int, int, int] = (200, 200, 200),
        font_size: int = 24,
    ):
        super().__init__(
            x, y, width, height, text_on, color, hover_color, font_size=font_size
        )
        self.text_on = text_on
        self.text_off = text_off
        self.toggled = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.toggled = not self.toggled
                self.text = self.text_on if self.toggled else self.text_off


class ToggleLightButton(ToggleButton):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text_on: str = "On",
        text_off: str = "Off",
        color_off: Tuple[int, int, int] = (200, 80, 80),
        color_on: Tuple[int, int, int] = (80, 200, 80),
        hover_color_off: Tuple[int, int, int] = (230, 110, 110),
        hover_color_on: Tuple[int, int, int] = (110, 230, 110),
        font_size: int = 24,
    ):
        super().__init__(
            x,
            y,
            width,
            height,
            text_on=text_on,
            text_off=text_off,
            color=color_off,
            hover_color=hover_color_off,
            font_size=font_size,
        )

        self.color_off = color_off
        self.color_on = color_on
        self.hover_color_off = hover_color_off
        self.hover_color_on = hover_color_on

        self.toggled = False
        self.text = text_off
        self.color = color_off
        self.hover_color = hover_color_off

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.toggled = not self.toggled
                if self.toggled:
                    self.text = self.text_on
                    self.color = self.color_on
                    self.hover_color = self.hover_color_on
                else:
                    self.text = self.text_off
                    self.color = self.color_off
                    self.hover_color = self.hover_color_off


class RangeInput:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        min_val: float,
        max_val: float,
        start_val: float,
        label: str = "",
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.label = label
        self.slider_rect = pygame.Rect(x, y, width, height)
        self.knob_x = self._value_to_x(start_val)
        self.dragging = False
        self.font = pygame.font.SysFont(None, 22)

    def _value_to_x(self, value: float) -> float:
        """Convert slider value to x-position."""
        return (
            self.x
            + ((value - self.min_val) / (self.max_val - self.min_val)) * self.width
        )

    def _x_to_value(self, x: float) -> float:
        """Convert x-position back to slider value."""
        ratio = (x - self.x) / self.width
        return self.min_val + ratio * (self.max_val - self.min_val)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if abs(event.pos[0] - self.knob_x) < 10 and self.slider_rect.collidepoint(
                event.pos
            ):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.value = round(self._x_to_value(self.knob_x), 2)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (200, 200, 200), self.slider_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.slider_rect, 2)

        pygame.draw.circle(
            screen, (100, 100, 255), (int(self.knob_x), self.y + self.height // 2), 8
        )

        label_text = f"{self.label}: {self.value:.1f} cars/s"
        text_surf = self.font.render(label_text, True, (0, 0, 0))
        screen.blit(text_surf, (self.x, self.y - 25))
