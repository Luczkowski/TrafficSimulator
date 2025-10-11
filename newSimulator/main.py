import pygame

from configuration import *
from road import Road

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

# --- Główna pętla ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for road in roads:
        road.spawn_car(cars)
        road.draw(screen)

    for car in cars[:]:
        car.draw(screen)
        car.update(cars, roads)

    pygame.display.flip()

pygame.quit()