import pygame

from configuration import *
from road import Road
from light import Light

# --- Pygame init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Symulacja 2.0")
clock = pygame.time.Clock()

# --- Inicjalizacja dróg ---
cars = []
roads = [
    Road((0, E_LANE), (WINDOW_WIDTH, E_LANE), "E", BLUE, ["N", "S", 'E']),
    Road((WINDOW_WIDTH, W_LANE), (0, W_LANE), "W", RED, ["N", "S", 'W']),
    Road((S_LANE, 0), (S_LANE, WINDOW_HEIGHT), "S", GREEN, ["E", "W", 'S']),
    Road((N_LANE, WINDOW_HEIGHT), (N_LANE, 0), "N", YELLOW, ["E", "W", 'N']),
]

stops = [
    Light(370, E_LANE + 8, phases=[(2, True), (4, False)]),
    Light(480, W_LANE + 8, phases=[(2, True), (4, False)]),
    Light(S_LANE + 8, 270, phases=[(3, False), (2, True), (1, False)]),
    Light(N_LANE + 8, 380, phases=[(3, False), (2, True), (1, False)]),
]

# --- Główna pętla ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for road in roads:
        road.spawn_car(cars, stops)
        road.draw(screen)

    for stop in stops:
        stop.draw(screen)
        stop.toggle_state()

    for car in cars[:]:
        car.draw(screen)
        car.update(cars, roads, stops)

    pygame.display.flip()

pygame.quit()