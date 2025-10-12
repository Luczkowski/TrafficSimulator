import pygame
import random
from collections import deque

from configuration import *
from car import Car
from drawing import draw_roads, draw_traffic_lights, draw_sidebar, draw_slider

# --- Pygame init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH + 200, WINDOW_HEIGHT))
pygame.display.set_caption("Symulacja pasa z zatrzymywaniem")
clock = pygame.time.Clock()

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
car_times = deque()

def handle_slider(event, spawn_interval, y_pos):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if WINDOW_WIDTH + 20 <= mouse_x <= WINDOW_WIDTH + 180 and y_pos <= mouse_y <= y_pos + 10:
        new_interval = max(min(mouse_x - (WINDOW_WIDTH + 20), 200 - 10), 10)
        return (new_interval * (200 - 10) // (WINDOW_WIDTH + 180 - (WINDOW_WIDTH + 20))) + 10
    return spawn_interval

def increment_cars_passed():
    global total_cars_passed
    car_times.append(elapsed_time)

# --- Główna pętla ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    # --- Eventy ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            E_SPAWN_INTERVAL = handle_slider(event, E_SPAWN_INTERVAL, 80)
            W_SPAWN_INTERVAL = handle_slider(event, W_SPAWN_INTERVAL, 120)
            S_SPAWN_INTERVAL = handle_slider(event, S_SPAWN_INTERVAL, 160)
            N_SPAWN_INTERVAL = handle_slider(event, N_SPAWN_INTERVAL, 200)

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
            spawn_car(0 - CAR_SIZE, E_LANE, 'E', BLUE, cars)
            e_spawn_timer = E_SPAWN_INTERVAL
    else:
        e_spawn_timer -= 1

    if w_spawn_timer <= 0:
        if random.random() < 0.05:
            spawn_car(WINDOW_WIDTH, W_LANE, 'W', RED, cars)
            w_spawn_timer = W_SPAWN_INTERVAL
    else:
        w_spawn_timer -= 1

    if s_spawn_timer <= 0:
        if random.random() < 0.05:
            spawn_car(S_LANE, 0 - CAR_SIZE, 'S', GREEN, cars)
            s_spawn_timer = S_SPAWN_INTERVAL
    else:
        s_spawn_timer -= 1

    if n_spawn_timer <= 0:
        if random.random() < 0.05:
            spawn_car(N_LANE, WINDOW_HEIGHT, 'N', YELLOW, cars)
            n_spawn_timer = N_SPAWN_INTERVAL
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
        while car_times and elapsed_time - car_times[0] > 15:
            car_times.popleft()
        cars_last_5s = len(car_times)
        cars_per_seconds = cars_last_5s / 15
        second_timer = 0

    font = pygame.font.SysFont('Arial', 16)
    text = font.render(f'Przepustowość: {cars_per_seconds:.2f} auta/s', True, WHITE)
    screen.blit(text, (10, 10))

    draw_roads(screen)
    draw_traffic_lights(screen, green_light_active, current_direction)
    draw_sidebar(screen)
    draw_slider(screen, E_SPAWN_INTERVAL, 80, "Niebieskie")
    draw_slider(screen, W_SPAWN_INTERVAL, 120, "Czerwone")
    draw_slider(screen, S_SPAWN_INTERVAL, 160, "Zielone")
    draw_slider(screen, N_SPAWN_INTERVAL, 200, "Żółte")
    pygame.display.flip()

pygame.quit()