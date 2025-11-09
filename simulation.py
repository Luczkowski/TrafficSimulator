import pygame

from car import Car
from clock import LightClock
from components.gui import RangeInput, RestartButton, StopButton, ToggleAutomaticControlButton, ToggleLightButton
from configuration import *
from light import Light
from road import Road


class Simulation:
    def __init__(self) -> None:
        # --- Stan symulacji ---
        self.running = True
        self.automatic_control = True

        # --- Drogi ---
        self.roads = [
            Road((0, int(E_LANE)), (WINDOW_WIDTH, int(E_LANE)), "E", BLUE, ["N", "S", "E"]),
            Road((WINDOW_WIDTH, int(W_LANE)), (0, int(W_LANE)), "W", RED, ["N", "S", "W"]),
            Road((int(S_LANE), 0), (int(S_LANE), WINDOW_HEIGHT), "S", GREEN, ["E", "W", "S"]),
            Road((int(N_LANE), WINDOW_HEIGHT), (int(N_LANE), 0), "N", YELLOW, ["E", "W", "N"]),
        ]

        # --- Sygnalizacja świetlna ---
        self.stops = [
            Light(370, int(E_LANE + 8), "E"),
            Light(480, int(W_LANE + 8), "W"),
            Light(int(S_LANE + 8), 270, "S"),
            Light(int(N_LANE + 8), 380, "N"),
        ]

        # --- Kolejka dla świateł ---
        self.lights_queue = LightClock([(("E", "W"), 3.0), (("N"), 3.0), (("S"), 1.0)])

        # --- Pojazdy ---
        self.cars: list[Car] = []

        # --- GUI ---
        self.gui = [
            StopButton(self.get_running, self.set_running),
            RestartButton(self.set_cars),
            ToggleAutomaticControlButton(self.get_automatic_control, self.set_automatic_control),
        ]

        self.light_buttons = []
        button_x = WINDOW_WIDTH - 200
        button_y = 20
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

        # --- Współczynnik pojawiania się nowych pojazdów ---
        self.spawn_sliders = [
            RangeInput(
                x=20,
                y=40 + i * 60,
                width=200,
                height=20,
                min_val=0,
                max_val=10.0,
                start_val=1.0,
                label=f"{road.name} spawn rate",
            )
            for i, road in enumerate(self.roads)
        ]

    # --- Getters & setters ---
    def get_running(self) -> bool:
        return self.running

    def get_automatic_control(self) -> bool:
        return self.automatic_control

    def set_running(self, state: bool) -> None:
        self.running = state

    def set_cars(self, new_cars: list[Car] | None = None) -> None:
        if new_cars is None:
            self.cars.clear()
        else:
            self.cars = new_cars

    def set_automatic_control(self, state: bool) -> None:
        self.automatic_control = state
        for light in self.stops:
            light.automatic_control = self.automatic_control

    def update(self, screen: pygame.Surface, dt: float) -> None:
        # GUI
        for gui_element in self.gui:
            gui_element.draw(screen)
        if not self.automatic_control:
            for button, _ in self.light_buttons:
                button.draw(screen)
            for slider in self.spawn_sliders:
                slider.draw(screen)

        # Simulation logic
        if self.running:
            if self.automatic_control:
                self.lights_queue.update(dt)
                for stop in self.stops:
                    stop.check_state(self.lights_queue.get_current_directions())

            for road, inp in zip(self.roads, self.spawn_sliders):
                cars_per_second = inp.value
                spawn_frequency = int(FPS / cars_per_second) if cars_per_second > 0 else 999999
                road.set_spawn_frequency(spawn_frequency)
                road.spawn_car(self.cars, self.stops)

            for car in self.cars[:]:
                car.update(self.cars, self.roads, self.stops)

        # Drawing
        for road in self.roads:
            road.draw(screen)
        for stop in self.stops:
            stop.draw(screen)
        for car in self.cars:
            car.draw(screen)
