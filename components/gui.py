import pygame
from configuration import *


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
        ),
        self.set_cars = set_cars

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                set_cars([])


class ToggleAutomaticControlButton(Button):
    pass
