import pygame
import random
from configuration import *

# --- Klasa Samochodu ---
class Car:
    def __init__(self, x, y, direction, color,increment_func):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.passed_stop = False
        self.turn = random.choice(['straight', 'right', 'left'])
        self.increment_func = increment_func

    def get_future_rect(self):
        future_x, future_y = self.x, self.y
        if self.direction == 'E':
            future_x += CAR_SPEED + 2
        if self.direction == 'W':
            future_x -= CAR_SPEED + 2
        if self.direction == 'S':
            future_y += CAR_SPEED + 2
        if self.direction == 'N':
            future_y -= CAR_SPEED + 2

        return pygame.Rect(future_x, future_y, CAR_SIZE, CAR_SIZE)

    def can_move(self, cars, green_light):
        if self.passed_stop:
            my_future_rect = self.get_future_rect()
            for other in cars:
                if other is self:
                    continue
                other_rect = pygame.Rect(other.x, other.y, CAR_SIZE, CAR_SIZE)
                if my_future_rect.colliderect(other_rect):
                    return False
            return True

        # Jeżeli jest czerwone i w następnej klatce samochód przekroczyłby linię stop
        # to nie może jechać dalej
        if self.direction == 'E':
            next_x = self.x + CAR_SPEED
            if not green_light and next_x + CAR_SIZE >= STOP_E:
                return False
        if self.direction == 'W':
            next_x = self.x - CAR_SPEED
            if not green_light and next_x < STOP_W:
                return False
        if self.direction == 'S':
            next_y = self.y + CAR_SPEED
            if not green_light and next_y + CAR_SIZE >= STOP_S:
                return False
        if self.direction == 'N':
            next_y = self.y - CAR_SPEED
            if not green_light and next_y < STOP_N:
                return False

        # Sprawdzenie potencjalnej kolizji
        my_future_rect = self.get_future_rect()
        for other in cars:
            if other is self:
                continue
            other_rect = pygame.Rect(other.x, other.y, CAR_SIZE, CAR_SIZE)
            if my_future_rect.colliderect(other_rect):
                return False
        return True

    def move(self):
        global car_passed

        if self.direction == 'E':
            self.x += CAR_SPEED
            if not self.passed_stop:
                if self.x + CAR_SIZE >= STOP_E:
                    self.passed_stop = True
                    self.increment_func()
            else:
                if self.turn == 'right' and self.x == S_LANE:
                    self.direction = 'S'
                    self.turn = 'straight'
                if self.turn == 'left' and self.x == N_LANE:
                    self.direction = 'N'
                    self.turn = 'straight'
        if self.direction == 'W':
            self.x -= CAR_SPEED
            if not self.passed_stop:
                if self.x < STOP_W:
                    self.passed_stop = True
                    self.increment_func()
            else:
                if self.turn == 'right' and self.x == N_LANE:
                    self.direction = 'N'
                    self.turn = 'straight'
                if self.turn == 'left' and self.x == S_LANE:
                    self.direction = 'S'
                    self.turn = 'straight'
        if self.direction == 'S':
            self.y += CAR_SPEED
            if not self.passed_stop:
                if self.y + CAR_SIZE >= STOP_S:
                    self.passed_stop = True
                    self.increment_func()
            else:
                if self.turn == 'right' and self.y == W_LANE:
                    self.direction = 'W'
                    self.turn = 'straight'
                if self.turn == 'left' and self.y == E_LANE:
                    self.direction = 'E'
                    self.turn = 'straight'
        if self.direction == 'N':
            self.y -= CAR_SPEED
            if not self.passed_stop:
                if self.y < STOP_N:
                    self.passed_stop = True
                    self.increment_func()
            else:
                if self.turn == 'right' and self.y == E_LANE:
                    self.direction = 'E'
                    self.turn = 'straight'
                if self.turn == 'left' and self.y == W_LANE:
                    self.direction = 'W'
                    self.turn = 'straight'

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, CAR_SIZE, CAR_SIZE)
        pygame.draw.rect(surface, self.color, rect)

    def is_offscreen(self):
        return self.x > WINDOW_WIDTH or self.x < 0 - CAR_SIZE or self.y > WINDOW_HEIGHT or self.y < 0 - CAR_SIZE
