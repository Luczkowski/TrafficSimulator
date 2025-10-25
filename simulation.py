import pygame
from configuration import *
from road import Road
from light import Light
from components.gui import (
    Button,
    StopButton,
    RestartButton,
    ToggleAutomaticControlButton,
    ToggleButton,
    ToggleLightButton,
)


class Simulation:
    def __init__(self):
        # --- Stan symulacji ---
        self.running = True
        self.automatic_control = True

        # --- Drogi ---
        self.roads = [
            Road((0, E_LANE), (WINDOW_WIDTH, E_LANE), "E", BLUE, ["N", "S", "E"]),
            Road((WINDOW_WIDTH, W_LANE), (0, W_LANE), "W", RED, ["N", "S", "W"]),
            Road((S_LANE, 0), (S_LANE, WINDOW_HEIGHT), "S", GREEN, ["E", "W", "S"]),
            Road((N_LANE, WINDOW_HEIGHT), (N_LANE, 0), "N", YELLOW, ["E", "W", "N"]),
        ]

        # --- Sygnalizacja świetlna ---
        self.stops = [
            Light(
                370, E_LANE + 8, phases=[(2, True), (4, False)], automatic_control=True
            ),
            Light(
                480, W_LANE + 8, phases=[(2, True), (4, False)], automatic_control=True
            ),
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

        # --- Pojazdy ---
        self.cars = []

        # --- GUI ---
        self.gui = [
            StopButton(self.get_running, self.set_running),
            RestartButton(self.set_cars),
            ToggleAutomaticControlButton(
                self.get_automatic_control, self.set_automatic_control
            ),
        ]

        self.light_buttons = []
        button_x = WINDOW_WIDTH-200
        button_y = 80
        for i, light in enumerate(self.stops):
            button = ToggleLightButton(
                x=button_x,
                y=button_y + i * 50,
                width=160,
                height=40,
                text_on=f"Light {i+1} ON",
                text_off=f"Light {i+1} OFF",
            )
            self.light_buttons.append((button, light))

    # --- Getters & setters ---
    def get_running(self):
        return self.running

    def get_automatic_control(self):
        return self.automatic_control

    def set_running(self, state: bool):
        self.running = state

    def set_cars(self, new_cars=None):
        if new_cars is None:
            self.cars.clear()
        else:
            self.cars = new_cars

    def set_automatic_control(self, state: bool):
        self.automatic_control = state
        for light in self.stops:
            light.automatic_control = self.automatic_control

    def update(self, screen):
        for gui_element in self.gui:
            gui_element.draw(screen)

        if not self.automatic_control:
            for button, _ in self.light_buttons:
                button.draw(screen)

        if self.running:
            for road in self.roads:
                road.spawn_car(self.cars, self.stops)
                road.draw(screen)

            for stop in self.stops:
                stop.draw(screen)
                stop.toggle_state()

            for car in self.cars[:]:
                car.update(self.cars, self.roads, self.stops)
                car.draw(screen)
        else:
            for road in self.roads:
                road.draw(screen)
            for stop in self.stops:
                stop.draw(screen)
            for car in self.cars:
                car.draw(screen)
