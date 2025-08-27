from os import EX_OK

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

CAR_SIZE = 20
CAR_SPEED = 2
SPAWN_INTERVAL = 60

LIGHT_SIZE = 20

Y_LANE = WINDOW_HEIGHT / 2
X_LANE = WINDOW_WIDTH / 2

# punkty zatrzymania
STOP_E = X_LANE - CAR_SIZE - 14
STOP_W = X_LANE + CAR_SIZE + 14
STOP_S = Y_LANE - CAR_SIZE - 14
STOP_N = Y_LANE + CAR_SIZE + 14

STOP_DURATION = 200  # czas trwania czerwonego światła w klatkach
STOP_INTERVAL = 200  # co ile klatek pojawia się czerwone światło

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
