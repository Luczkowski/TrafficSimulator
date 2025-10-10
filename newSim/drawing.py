import pygame
from configuration import *

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

def draw_sidebar(screen):
    # Panel boczny
    sidebar_width = 200
    pygame.draw.rect(screen, DARK_GRAY, pygame.Rect(WINDOW_WIDTH, 0, sidebar_width, WINDOW_HEIGHT))

    # Tytuł
    font = pygame.font.SysFont('Arial', 20)
    title_text = font.render("Auta na sekundę:", True, WHITE)
    screen.blit(title_text, (WINDOW_WIDTH + 20, 20))

def draw_slider(screen, value, y_pos, label):
    pygame.draw.line(screen, WHITE, (WINDOW_WIDTH + 20, y_pos + 5), (WINDOW_WIDTH + 180, y_pos + 5), 2)
    knob_x = WINDOW_WIDTH + 20 + int((value - 10) * (160 / (200 - 10)))
    pygame.draw.circle(screen, RED, (knob_x, y_pos + 5), 6)
    cars_per_second = round(60 / value, 2) if value > 0 else 0
    font = pygame.font.SysFont('Arial', 16)
    text = font.render(f"{label}: {cars_per_second}", True, WHITE)
    screen.blit(text, (WINDOW_WIDTH + 20, y_pos - 20))
