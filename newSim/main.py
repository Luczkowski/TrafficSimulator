import pygame

from configuration import *
from road import Road

# --- Pygame init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Symulacja skrzyżowania bez świateł")
clock = pygame.time.Clock()

# --- Inicjalizacja ---
cars = []
roads = [
    Road((0, E_LANE), (WINDOW_WIDTH, E_LANE), (STOP_E, E_LANE), "E", BLUE, ["N", "S"]),
    Road((WINDOW_WIDTH, W_LANE), (0, W_LANE), (STOP_W, W_LANE), "W", RED, ["N", "S"]),
    Road((S_LANE, 0), (S_LANE, WINDOW_HEIGHT), (S_LANE, STOP_S), "S", GREEN, ["E", "W"]),
    Road((N_LANE, WINDOW_HEIGHT), (N_LANE, 0), (N_LANE, STOP_N), "N", YELLOW, ["E", "W"]),
]

letter_sequence = [("NS", 4000), ("EW", 4000)]
current_letter_index = 0
letter_start_time = pygame.time.get_ticks()
font = pygame.font.SysFont(None, 72)

# --- Główna pętla ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    # --- Aktualizacja liter ---
    current_time = pygame.time.get_ticks()
    current_letter, display_time = letter_sequence[current_letter_index]

    if current_time - letter_start_time >= display_time:
        current_letter_index = (current_letter_index + 1) % len(letter_sequence)
        letter_start_time = current_time

    # --- Rysowanie liter ---
    #text_surface = font.render(current_letter, True, BLACK)
    #text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))  # wyświetlanie na górze
    #screen.blit(text_surface, text_rect)

    # --- Eventy ---
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