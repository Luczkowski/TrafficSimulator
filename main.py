import tkinter as tk
import threading
import time
import random

# === KOLEJKI AUT ===
traffic_straight = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
traffic_left = {'N': 0, 'S': 0, 'E': 0, 'W': 0}

# === KOLEJKI PIESZYCH ===
pedestrians = {'N': 0, 'S': 0, 'E': 0, 'W': 0}

active_phase = 'NS_straight'
lock = threading.Lock()

CIRCLE_RADIUS = 8
UPDATE_INTERVAL = 1000  # ms

class TrafficApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skrzyżowanie z lewoskrętami + piesi")
        self.canvas = tk.Canvas(root, width=550, height=550, bg='lightgrey')
        self.canvas.pack()

        self.light_ids = {}
        self.text_ids = {}

        self.ped_light_ids = {}  # światła dla pieszych
        self.ped_text_ids = {}   # liczniki pieszych

        self.draw_intersection()
        self.update_gui()

    def draw_intersection(self):
        self.canvas.create_rectangle(225, 0, 325, 550, fill='darkgrey')  # pion
        self.canvas.create_rectangle(0, 225, 550, 325, fill='darkgrey')  # poziom

        positions = {
            'N': (275, 90),
            'S': (275, 460),
            'E': (460, 275),
            'W': (90, 275)
        }

        for d, (x, y) in positions.items():
            # światła aut
            l_main = self.canvas.create_oval(x - CIRCLE_RADIUS, y - CIRCLE_RADIUS,
                                             x + CIRCLE_RADIUS, y + CIRCLE_RADIUS,
                                             fill='red')
            l_left = self.canvas.create_oval(x - CIRCLE_RADIUS - 20, y - CIRCLE_RADIUS,
                                             x + CIRCLE_RADIUS - 20, y + CIRCLE_RADIUS,
                                             fill='red')

            txt = self.canvas.create_text(x, y + 28,
                                          text=f"{d} →0 | ←0",
                                          font=("Arial", 9), justify='center')

            # światła pieszych
            ped_x, ped_y = x + 30, y - 20
            l_ped = self.canvas.create_rectangle(ped_x, ped_y,
                                                 ped_x + 12, ped_y + 12,
                                                 fill='red')
            txt_ped = self.canvas.create_text(ped_x + 6, ped_y + 20,
                                              text="0", font=("Arial", 8))

            self.light_ids[d] = {'main': l_main, 'left': l_left}
            self.text_ids[d] = txt
            self.ped_light_ids[d] = l_ped
            self.ped_text_ids[d] = txt_ped

    def update_gui(self):
        with lock:
            for d in ['N', 'S', 'E', 'W']:
                # światła aut
                main_green = active_phase in ['NS_straight', 'EW_straight'] and d in active_phase
                left_green = active_phase in ['NS_left', 'EW_left'] and d in active_phase

                self.canvas.itemconfig(self.light_ids[d]['main'], fill='green' if main_green else 'red')
                self.canvas.itemconfig(self.light_ids[d]['left'], fill='green' if left_green else 'red')

                # licznik aut
                c_straight = traffic_straight[d]
                c_left = traffic_left[d]
                self.canvas.itemconfig(self.text_ids[d], text=f"{d} ←{c_left} | →{c_straight}")

                # piesi
                ped_green = d in pedestrian_green_dirs(active_phase)
                self.canvas.itemconfig(self.ped_light_ids[d], fill='green' if ped_green else 'red')
                self.canvas.itemconfig(self.ped_text_ids[d], text=str(pedestrians[d]))

        self.root.after(UPDATE_INTERVAL, self.update_gui)

# === FUNKCJE LOGICZNE ===

def pedestrian_green_dirs(phase):
    """Zwraca listę kierunków, w których piesi mają zielone światło"""
    if phase == 'NS_straight':
        return ['E', 'W']
    elif phase == 'EW_straight':
        return ['N', 'S']
    return []  # piesi nie mają zielonego w fazie lewoskrętów

def car_generator():
    directions = ['N', 'S', 'E', 'W']
    while True:
        time.sleep(random.uniform(0.4, 1.2))
        d = random.choice(directions)
        turn = random.choice(['straight', 'left'])

        with lock:
            if turn == 'straight':
                traffic_straight[d] += 1
            else:
                traffic_left[d] += 1

def pedestrian_generator():
    directions = ['N', 'S', 'E', 'W']
    while True:
        time.sleep(random.uniform(2, 4))  # piesi rzadziej
        d = random.choice(directions)
        with lock:
            pedestrians[d] += 1

def traffic_light_controller():
    global active_phase
    phases = ['NS_straight', 'NS_left', 'EW_straight', 'EW_left']
    while True:
        for phase in phases:
            with lock:
                active_phase = phase
            time.sleep(4)

def car_remover():
    while True:
        with lock:
            for d in ['N', 'S', 'E', 'W']:
                if active_phase.endswith('straight') and d in active_phase:
                    passed = min(traffic_straight[d], random.randint(1, 3))
                    traffic_straight[d] -= passed
                elif active_phase.endswith('left') and d in active_phase:
                    passed = min(traffic_left[d], random.randint(1, 2))
                    traffic_left[d] -= passed
        time.sleep(1.5)

def pedestrian_remover():
    while True:
        with lock:
            dirs = pedestrian_green_dirs(active_phase)
            for d in dirs:
                passed = min(pedestrians[d], random.randint(1, 2))
                pedestrians[d] -= passed
        time.sleep(1.5)

# === URUCHOMIENIE WĄTKÓW I GUI ===
threading.Thread(target=car_generator, daemon=True).start()
threading.Thread(target=pedestrian_generator, daemon=True).start()
threading.Thread(target=traffic_light_controller, daemon=True).start()
threading.Thread(target=car_remover, daemon=True).start()
threading.Thread(target=pedestrian_remover, daemon=True).start()

root = tk.Tk()
app = TrafficApp(root)
root.mainloop()
