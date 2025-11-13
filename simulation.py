import pygame

from car import Car
from clock import LightClock
from components.gui import (
    RangeInput,
    RestartButton,
    StopButton,
    ToggleAutomaticControlButton,
    ToggleLightButton,
)
from configuration import *
from light import Light
from road import Road


class Simulation:
    def __init__(self) -> None:
        # --- Simulation states ---
        self.running = True
        self.automatic_control = True

        # --- Roads ---
        self.roads = [
            Road(
                (int(S_LANE), 0),
                (int(S_LANE), WINDOW_HEIGHT),
                "CHLOPSKA S",
                (4, 0, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "PIASTOWSKA W",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
                spawn_rate=0.75,
            ),
            Road(
                (int(N_LANE), WINDOW_HEIGHT),
                (int(N_LANE), 0),
                "CHLOPSKA N",
                (66, 63, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "PIASTOWSKA W",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
                spawn_rate=1.1,
            ),
            Road(
                (WINDOW_WIDTH, 200),
                (0, 200),
                "PIASTOWSKA W",
                (2, 210, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "PIASTOWSKA W",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
                spawn_rate=0.1,
            ),
            Road(
                (0, 240),
                (WINDOW_WIDTH, 240),
                "PIASTOWSKA E",
                (70, 222, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
                spawn_rate=0.1,
            ),
            Road(
                (WINDOW_WIDTH, 400),
                (0, 400),
                "JAGIELLONSKA W",
                (2, 152, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "PIASTOWSKA W",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
            ),
            Road(
                (0, 440),
                (WINDOW_WIDTH, 440),
                "JAGIELLONSKA E",
                (70, 179, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "PIASTOWSKA W",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
            ),
            Road(
                (WINDOW_WIDTH, 600),
                (0, 600),
                "KOLOBRZESKA W",
                (2, 81, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "PIASTOWSKA W",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
                spawn_rate=1.25,
            ),
            Road(
                (0, 640),
                (WINDOW_WIDTH, 640),
                "KOLOBRZESKA E",
                (63, 123, 252),
                [
                    "CHLOPSKA N",
                    "CHLOPSKA S",
                    "PIASTOWSKA E",
                    "PIASTOWSKA W",
                    "JAGIELLONSKA E",
                    "JAGIELLONSKA W",
                    "KOLOBRZESKA E",
                    "KOLOBRZESKA W",
                ],
                spawn_rate=1.25,
            ),
        ]

        # --- Traffic lights ---
        self.stops = [
            # CHLOPSKA
            Light(792, 180, "S"),
            Light(792, 380, "S"),
            Light(792, 580, "S"),
            Light(850, 264, "N"),
            Light(850, 464, "N"),
            Light(850, 664, "N"),
            # Piastowska
            Light(874, 202, "W"),
            Light(772, 242, "E"),
            # JAGIELLONSKA
            Light(874, 402, "W"),
            Light(772, 442, "E"),
            # KOLOBRZESKA
            Light(874, 602, "W"),
            Light(772, 642, "E"),
        ]

        # --- Lights queues ---
        self.lights_queue = LightClock(
            [(("N", "S"), 10.0), (None, 2), (("E", "W"), 6.0), (None, 2)]
        )

        # --- Cars ---
        self.cars: list[Car] = []

        # --- GUI ---
        self.gui = [
            StopButton(self.get_running, self.set_running),
            RestartButton(self.set_cars),
            ToggleAutomaticControlButton(
                self.get_automatic_control, self.set_automatic_control
            ),
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

        # --- Spawn rate sliders ---
        self.spawn_sliders = [
            RangeInput(
                x=20,
                y=40 + i * 60,
                width=200,
                height=20,
                min_val=0,
                max_val=10.0,
                start_val=self.roads[i].spawn_rate,
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

        if self.automatic_control:
            for i, road in enumerate(self.roads):
                road.set_spawn_rate(road.default_spawn_rate)
                if i < len(self.spawn_sliders):
                    self.spawn_sliders[i].value = road.spawn_rate
                    self.spawn_sliders[i].knob_x = self.spawn_sliders[
                        i
                    ]._value_to_x(self.spawn_sliders[i].value)

    def update(self, screen: pygame.Surface, dt: float) -> None:
        for gui_element in self.gui:
            gui_element.draw(screen)
        if not self.automatic_control:
            for button, _ in self.light_buttons:
                button.draw(screen)
            for slider in self.spawn_sliders:
                slider.draw(screen)

        # SIMULATION LOGIC
        if self.running:
            if self.automatic_control:
                self.lights_queue.update(dt)
                for stop in self.stops:
                    stop.check_state(self.lights_queue.get_current_directions())

            for road, slider in zip(self.roads, self.spawn_sliders):
                if abs(road.spawn_rate - slider.value) > 1e-6:  # rate changed
                    road.set_spawn_rate(slider.value)
                road.spawn_car(self.cars, self.stops, dt)

            for car in self.cars[:]:
                car.update(self.cars, self.roads, self.stops)

        for road in self.roads:
            road.draw(screen)
        for stop in self.stops:
            stop.draw(screen)
        for car in self.cars:
            car.draw(screen)
