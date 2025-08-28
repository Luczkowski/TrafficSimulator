import pygame
import random
from configuration import *

# --- Pygame init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Symulacja pasa z zatrzymywaniem")
clock = pygame.time.Clock()

# --- Klasa Samochodu ---
class Car:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.passed_stop = False

    def can_move(self, cars, green_light):
        if self.passed_stop:
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

        # Sprawdzenie odległości od samochodu z przodu
        for other in cars:
            if other is self:
                continue

            if self.direction == 'E':
                if other.x > self.x:
                    distance = other.x - (self.x + CAR_SIZE)
                    if distance < 4:
                        return False
            if self.direction == 'W':
                if other.x < self.x:
                    distance = self.x - (other.x + CAR_SIZE)
                    if distance < 4:
                        return False
            if self.direction == 'S':
                if other.y > self.y:
                    distance = other.y - (self.y + CAR_SIZE)
                    if distance < 4:
                        return False
            if self.direction == 'N':
                if other.y < self.y:
                    distance = self.y - (other.y + CAR_SIZE)
                    if distance < 4:
                        return False
        return True

    def move(self):
        if self.direction == 'E':
            self.x += CAR_SPEED
            if not self.passed_stop:
                if self.x + CAR_SIZE >= STOP_E:
                    self.passed_stop = True
        if self.direction == 'W':
            self.x -= CAR_SPEED
            if not self.passed_stop:
                if self.x < STOP_W:
                    self.passed_stop = True
        if self.direction == 'S':
            self.y += CAR_SPEED
            if not self.passed_stop:
                if self.y + CAR_SIZE >= STOP_S:
                    self.passed_stop = True
        if self.direction == 'N':
            self.y -= CAR_SPEED
            if not self.passed_stop:
                if self.y < STOP_N:
                    self.passed_stop = True

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, CAR_SIZE, CAR_SIZE)
        pygame.draw.rect(surface, self.color, rect)

    def is_offscreen(self):
        return self.x > WINDOW_WIDTH or self.x < 0 - CAR_SIZE or self.y > WINDOW_HEIGHT or self.y < 0 - CAR_SIZE

def draw_traffic_lights(surface, green_light, direction):
    # Światło dla E
    e_color = GREEN if green_light and direction == 'W' else RED
    e_rect = pygame.Rect(STOP_E - LIGHT_SIZE - 5, Y_LANE + CAR_SIZE + 14, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(surface, e_color, e_rect)
    # Światło dla W
    w_color = GREEN if green_light and direction == 'W' else RED
    w_rect = pygame.Rect(STOP_W + 5, Y_LANE - LIGHT_SIZE - CAR_SIZE - 14, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(surface, w_color, w_rect)
    # Światło dla S
    s_color = GREEN if green_light and direction == 'N' else RED
    s_rect = pygame.Rect(X_LANE - LIGHT_SIZE - CAR_SIZE - 14, STOP_S - LIGHT_SIZE - 5, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(surface, s_color, s_rect)
    # Światło dla N
    n_color = GREEN if green_light and direction == 'N' else RED
    n_rect = pygame.Rect(X_LANE + CAR_SIZE + 14, STOP_N + 5, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(surface, n_color, n_rect)

# --- Inicjalizacja ---
e_lane_cars = []
w_lane_cars = []
s_lane_cars = []
n_lane_cars = []

e_spawn_timer = 0
w_spawn_timer = 0
s_spawn_timer = 0
n_spawn_timer = 0

green_light_active = False
current_direction = 'N'
light_timer = 0
pause_timer = 0

# --- Główna pętla ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    # --- Eventy ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pause_timer > 0:
        pause_timer -= 1
        green_light_active = False
    else:
        if light_timer > 0:
            light_timer -= 1
            green_light_active = True
        else:
            if current_direction == 'N':
                current_direction = 'W'
                light_timer = GREEN_TIME_W
            elif current_direction == 'W':
                current_direction = 'N'
                light_timer = GREEN_TIME_N
            # elif current_direction == 'S':
            #     current_direction = 'E'
            #     light_timer = GREEN_TIME_E
            # elif current_direction == 'E':
            #     current_direction = 'N'
            #     light_timer = GREEN_TIME_N

            pause_timer = PAUSE_TIME
            green_light_active = False

    # --- Spawning aut ---
    if e_spawn_timer <= 0:
        if random.random() < 0.05:
            car = Car(x=0, y=Y_LANE+5, direction='E', color=BLUE)
            e_lane_cars.append(car)
            e_spawn_timer = SPAWN_INTERVAL
    else:
        e_spawn_timer -= 1

    if w_spawn_timer <= 0:
        if random.random() < 0.05:
            car = Car(x=WINDOW_WIDTH - CAR_SIZE, y=Y_LANE-CAR_SIZE-5, direction='W', color=RED)
            w_lane_cars.append(car)
            w_spawn_timer = SPAWN_INTERVAL
    else:
        w_spawn_timer -= 1

    if s_spawn_timer <= 0:
        if random.random() < 0.05:
            car = Car(x=X_LANE-CAR_SIZE-5, y=0, direction='S', color=GREEN)
            s_lane_cars.append(car)
            s_spawn_timer = SPAWN_INTERVAL
    else:
        s_spawn_timer -= 1

    if n_spawn_timer <= 0:
        if random.random() < 0.05:
            car = Car(x=X_LANE+5, y=WINDOW_HEIGHT - CAR_SIZE, direction='N', color=YELLOW)
            n_lane_cars.append(car)
            n_spawn_timer = SPAWN_INTERVAL
    else:
        n_spawn_timer -= 1

    # --- Ruch samochodów ---
    for car in e_lane_cars:
        if car.can_move(e_lane_cars, green_light_active and current_direction == 'W'):
            car.move()
        car.draw(screen)

    for car in w_lane_cars:
        if car.can_move(w_lane_cars, green_light_active and current_direction == 'W'):
            car.move()
        car.draw(screen)

    for car in s_lane_cars:
        if car.can_move(s_lane_cars, green_light_active and current_direction == 'N'):
            car.move()
        car.draw(screen)

    for car in n_lane_cars:
        if car.can_move(n_lane_cars, green_light_active and current_direction == 'N'):
            car.move()
        car.draw(screen)

    # --- Usuwanie poza ekranem ---
    e_lane_cars = [car for car in e_lane_cars if not car.is_offscreen()]
    w_lane_cars = [car for car in w_lane_cars if not car.is_offscreen()]
    s_lane_cars = [car for car in s_lane_cars if not car.is_offscreen()]
    n_lane_cars = [car for car in n_lane_cars if not car.is_offscreen()]

    # --- Linie pasów ---
    # E
    pygame.draw.line(screen, WHITE, (0, Y_LANE + 1), (WINDOW_WIDTH, Y_LANE + 1), 2)
    pygame.draw.line(screen, WHITE, (0, Y_LANE + CAR_SIZE + 7), (WINDOW_WIDTH, Y_LANE + CAR_SIZE + 7), 2)
    # W
    pygame.draw.line(screen, WHITE, (0, Y_LANE - CAR_SIZE - 9), (WINDOW_WIDTH, Y_LANE - CAR_SIZE - 9), 2)
    pygame.draw.line(screen, WHITE, (0, Y_LANE - 3), (WINDOW_WIDTH, Y_LANE - 3), 2)
    # S
    pygame.draw.line(screen, WHITE, (X_LANE - CAR_SIZE - 9, 0), (X_LANE - CAR_SIZE - 9, WINDOW_HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (X_LANE - 3, 0), (X_LANE - 3, WINDOW_HEIGHT), 2)
    # N
    pygame.draw.line(screen, WHITE, (X_LANE + 1, 0), (X_LANE + 1, WINDOW_HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (X_LANE + CAR_SIZE + 7, 0), (X_LANE + CAR_SIZE + 7, WINDOW_HEIGHT), 2)

    draw_traffic_lights(screen, green_light_active, current_direction)
    pygame.display.flip()

pygame.quit()