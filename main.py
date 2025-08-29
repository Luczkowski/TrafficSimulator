import pygame
import random
from configuration import *
from car import Car

# --- Pygame init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Symulacja pasa z zatrzymywaniem")
clock = pygame.time.Clock()

# --- Rysowanie ---
def draw_traffic_lights(screen, green_light, direction):
    # Światło dla E
    e_color = GREEN if green_light and direction == 'W' else RED
    e_rect = pygame.Rect(STOP_E - CAR_SIZE, E_LANE + CAR_SIZE + 2, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(screen, e_color, e_rect)
    # Światło dla W
    w_color = GREEN if green_light and direction == 'W' else RED
    w_rect = pygame.Rect(STOP_W + CAR_SIZE - LIGHT_SIZE, W_LANE - LIGHT_SIZE, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(screen, w_color, w_rect)
    # Światło dla S
    s_color = GREEN if green_light and direction == 'N' else RED
    s_rect = pygame.Rect(S_LANE - LIGHT_SIZE, STOP_S - CAR_SIZE, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(screen, s_color, s_rect)
    # Światło dla N
    n_color = GREEN if green_light and direction == 'N' else RED
    n_rect = pygame.Rect(N_LANE + CAR_SIZE + 2, STOP_N + CAR_SIZE - LIGHT_SIZE, LIGHT_SIZE, LIGHT_SIZE)
    pygame.draw.rect(screen, n_color, n_rect)

def draw_roads(screen):
    # E
    pygame.draw.line(screen, WHITE, (0, E_LANE), (WINDOW_WIDTH, E_LANE), 2)
    pygame.draw.line(screen, WHITE, (0, E_LANE + CAR_SIZE), (WINDOW_WIDTH, E_LANE + CAR_SIZE), 2)
    # W
    pygame.draw.line(screen, WHITE, (0, W_LANE), (WINDOW_WIDTH, W_LANE), 2)
    pygame.draw.line(screen, WHITE, (0, W_LANE + CAR_SIZE), (WINDOW_WIDTH, W_LANE + CAR_SIZE), 2)
    # S
    pygame.draw.line(screen, WHITE, (S_LANE, 0), (S_LANE, WINDOW_HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (S_LANE + CAR_SIZE, 0), (S_LANE + CAR_SIZE, WINDOW_HEIGHT), 2)
    # N
    pygame.draw.line(screen, WHITE, (N_LANE, 0), (N_LANE, WINDOW_HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (N_LANE + CAR_SIZE, 0), (N_LANE + CAR_SIZE, WINDOW_HEIGHT), 2)

# --- Spawn samochodów ---
def can_spawn_new_car(x, y, cars):
    new_car_rect = pygame.Rect(x, y, CAR_SIZE, CAR_SIZE)
    for car in cars:
        car_rect = pygame.Rect(car.x, car.y, CAR_SIZE, CAR_SIZE)
        if new_car_rect.colliderect(car_rect):
            return False
    return True

def spawn_car(x, y, direction, color, cars):
    if can_spawn_new_car(x, y, cars):
        car = Car(x, y, direction, color, increment_func=increment_cars_passed)
        cars.append(car)
        return True
    return False

# --- Inicjalizacja ---
cars = []

e_spawn_timer = 0
w_spawn_timer = 0
s_spawn_timer = 0
n_spawn_timer = 0

green_light_active = False
current_direction = 'N'
light_timer = 0
pause_timer = 0
cars_per_seconds = 0
total_cars_passed = 0
elapsed_time = 0
second_timer = 0

def increment_cars_passed():
    global total_cars_passed
    total_cars_passed += 1

# --- Główna pętla ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    # --- Eventy ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Zmiana świateł ---
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

    # --- Spawn samochodów ---
    if e_spawn_timer <= 0:
        if random.random() < 0.05:
            spawn_car(0-CAR_SIZE, E_LANE, 'E', BLUE, cars)
            e_spawn_timer = SPAWN_INTERVAL
    else:
        e_spawn_timer -= 1

    if w_spawn_timer <= 0:
        if random.random() < 0.05:
            spawn_car(WINDOW_WIDTH, W_LANE, 'W', RED, cars)
            w_spawn_timer = SPAWN_INTERVAL
    else:
        w_spawn_timer -= 1

    if s_spawn_timer <= 0:
        if random.random() < 0.05:

            spawn_car(S_LANE, 0-CAR_SIZE, 'S', GREEN, cars)
            s_spawn_timer = SPAWN_INTERVAL
    else:
        s_spawn_timer -= 1

    if n_spawn_timer <= 0:
        if random.random() < 0.05:
            spawn_car(N_LANE, WINDOW_HEIGHT, 'N', YELLOW, cars)
            n_spawn_timer = SPAWN_INTERVAL
    else:
        n_spawn_timer -= 1

    # --- Ruch samochodów ---
    for car in cars:
        green = green_light_active and (
            (car.direction in ['E', 'W'] and current_direction == 'W') or
            (car.direction in ['N', 'S'] and current_direction == 'N')
        )
        if car.can_move(cars, green):
            car.move()
        car.draw(screen)

    # --- Usuwanie poza ekranem ---
    cars = [car for car in cars if not car.is_offscreen()]

    second_timer += 1 / FPS
    elapsed_time += 1 / FPS

    if second_timer >= 1:
        cars_per_seconds = (total_cars_passed / elapsed_time) if elapsed_time > 0 else 0
        second_timer = 0

    font = pygame.font.SysFont('Arial', 12)
    text = font.render(f'Przepustowość: {cars_per_seconds:.2f} auta/s', True, WHITE)
    screen.blit(text, (10, 10))

    draw_roads(screen)
    draw_traffic_lights(screen, green_light_active, current_direction)
    pygame.display.flip()

pygame.quit()