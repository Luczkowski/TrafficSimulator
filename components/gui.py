import pygame
from configuration import *


# Buttons
class Button:
    def __init__(
        self, x, y, width, height, text, color, hover_color, action=None, font_size=24
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


class StopButton(Button):
    def __init__(self, get_simulation_state, set_simulation_state):
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                new_state = not self.get_simulation_state()
                self.set_simulation_state(new_state)

                self.text = "Stop" if new_state else "Start"


class RestartButton(Button):
    def __init__(self, set_cars):
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.set_cars([])


class ToggleAutomaticControlButton(Button):
    def __init__(self, get_automatic_control, set_automatic_control):
        super().__init__(
            20,
            20,
            160,
            40,
            "Automatic mode",
            (180, 180, 180),
            (200, 200, 200),
            action=None,
        )
        self.get_automatic_control = get_automatic_control
        self.set_automatic_control = set_automatic_control

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.set_automatic_control(not self.get_automatic_control())
                if self.get_automatic_control() == True:
                    self.text = "Automatic control"
                else:
                    self.text = "Manual control"


class ToggleButton(Button):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text_on="On",
        text_off="Off",
        color=(180, 180, 180),
        hover_color=(200, 200, 200),
        font_size=24,
    ):
        super().__init__(
            x, y, width, height, text_on, color, hover_color, font_size=font_size
        )
        self.text_on = text_on
        self.text_off = text_off
        self.toggled = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.toggled = not self.toggled
                self.text = self.text_on if self.toggled else self.text_off


class ToggleLightButton(ToggleButton):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text_on="On",
        text_off="Off",
        color_off=(200, 80, 80),
        color_on=(80, 200, 80),
        hover_color_off=(230, 110, 110),
        hover_color_on=(110, 230, 110),
        font_size=24,
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

    def handle_event(self, event):
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
