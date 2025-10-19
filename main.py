import pygame

from configuration import *
from road import Road
from light import Light
from components.gui import Button, StopButton, RestartButton

# --- Pygame init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Symulacja 2.0")
clock = pygame.time.Clock()

# --- Logika symulacji ---
simulation_running = True
automatic_control = True


def get_simulation_state():
    return simulation_running


def set_simulation_state(state):
    global simulation_running
    simulation_running = state


def get_cars():
    return cars


def set_cars(new_cars):
    global cars
    cars = new_cars


# def reset_simulation():
#     global cars
#     cars.clear()


def toggle_automatic_control():
    global automatic_control, stops
    automatic_control = not automatic_control
    for light in stops:
        light.automatic_control = automatic_control
    if automatic_control:
        buttons[2].text = "Automatic mode"
    else:
        buttons[2].text = "Manual mode"


# --- Inicjalizacja interfejsu ---
buttons = [
    StopButton(get_simulation_state, set_simulation_state),
    RestartButton(set_cars),
    Button(
        20,
        20,
        160,
        40,
        "Automatic mode",
        (180, 180, 180),
        (200, 200, 200),
        toggle_automatic_control,
    ),
]


# --- Inicjalizacja drogi ---
cars = []
roads = [
    Road((0, E_LANE), (WINDOW_WIDTH, E_LANE), "E", BLUE, ["N", "S", "E"]),
    Road((WINDOW_WIDTH, W_LANE), (0, W_LANE), "W", RED, ["N", "S", "W"]),
    Road((S_LANE, 0), (S_LANE, WINDOW_HEIGHT), "S", GREEN, ["E", "W", "S"]),
    Road((N_LANE, WINDOW_HEIGHT), (N_LANE, 0), "N", YELLOW, ["E", "W", "N"]),
]

stops = [
    Light(370, E_LANE + 8, phases=[(2, True), (4, False)], automatic_control=True),
    Light(480, W_LANE + 8, phases=[(2, True), (4, False)], automatic_control=True),
    Light(
        S_LANE + 8,
        270,
        phases=[(3, False), (2, True), (1, False)],
        automatic_control=True,
    ),
    Light(
        N_LANE + 8,
        380,
        phases=[(3, False), (2, True), (1, False)],
        automatic_control=True,
    ),
]

# --- Główna pętla ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)

    for button in buttons:
        button.draw(screen)

    # --- Wydarzenia ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    # --- Logika symulacji ---
    if simulation_running:
        for road in roads:
            road.spawn_car(cars, stops)
            road.draw(screen)

        for stop in stops:
            stop.draw(screen)
            stop.toggle_state()

        for car in cars[:]:
            car.draw(screen)
            car.update(cars, roads, stops)
    else:
        for road in roads:
            road.draw(screen)
        for stop in stops:
            stop.draw(screen)
        for car in cars:
            car.draw(screen)

    pygame.display.flip()

pygame.quit()
