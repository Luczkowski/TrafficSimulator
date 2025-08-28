from os import EX_OK

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

CAR_SIZE = 20
CAR_SPEED = 2
SPAWN_INTERVAL = 80

LIGHT_SIZE = 20

Y_LANE = WINDOW_HEIGHT / 2
X_LANE = WINDOW_WIDTH / 2

# punkty zatrzymania
STOP_E = X_LANE - CAR_SIZE - 14
STOP_W = X_LANE + CAR_SIZE + 14
STOP_S = Y_LANE - CAR_SIZE - 14
STOP_N = Y_LANE + CAR_SIZE + 14

STOP_DURATION = FPS * 4  # czas trwania czerwonego światła w sekundach
STOP_INTERVAL = FPS * 4  # co ile sekund pojawia się czerwone światło

# Czas trwania zielonego światła (w klatkach, przy FPS = 60)
GREEN_TIME_E = 3 * FPS
GREEN_TIME_W = 3 * FPS
GREEN_TIME_S = 3 * FPS
GREEN_TIME_N = 3 * FPS
PAUSE_TIME = FPS

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
