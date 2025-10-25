import pygame
from configuration import *
from simulation import Simulation

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Symulacja 2.0")
clock = pygame.time.Clock()

sim = Simulation()

app_running = True
while app_running:
    clock.tick(FPS)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False

        for gui_element in sim.gui:
            gui_element.handle_event(event)

        if not sim.automatic_control:
            for button, light in sim.light_buttons:
                button.handle_event(event)
                if button.toggled:
                    light.set_state(True)
                else:
                    light.set_state(False)

    sim.update(screen)
    pygame.display.flip()

pygame.quit()
