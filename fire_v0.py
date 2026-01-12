import random
import time

HEIGHT = 20
WIDTH = 20
TEMPERATURE_LOSS = 20
CHANCE_TO_DISAPPEAR = 0.0

def clear():
    print("\033[2J\033[H", end="")

def rgb_print(text, rgb, **kwargs):
    r, g, b = rgb
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", **kwargs)
    
def fire_color(value):
    value = max(0, min(255, value))

    if value < 85:
        return (value * 3, 0, 0)
    elif value < 170:
        v = value - 85
        return (255, v * 3, 0)
    else:
        v = value - 170
        return (255, 255, v * 3)


class FireSimulation:
    def __init__(self, height, width, temperature_loss=30, chance_to_disappear=0.5):
        self.height = height
        self.width = width
        
        self.matrix = self.get_initial_matrix()
        self.temperature_loss = temperature_loss
        self.chance_to_disappear = chance_to_disappear
    
    def get_initial_matrix(self, temperature=250):
        initial_matrix = [
            [0 for _ in range(self.width)] for _ in range(self.height - 1)
        ]
        
        last_row = [temperature for _ in range(self.width)]
        initial_matrix.append(last_row)
        return initial_matrix
    
    def update(self):
        last_y = self.height - 1
        for y in range(last_y):
            for x in range(self.width):
                direction = self.get_direction()
                self.go_up(x, y, direction)
                
        for x in range(self.width):
            self.go_up(x, last_y, reset=False)
            
    def get_direction(self):
        random_value = random.random()
        
        if random_value < 0.1:
            return -1
        elif random_value < 0.9:
            return 0
        else:
            return 1
                
    def go_up(self, x, y, direciton=0, reset=True,):
        value = self.matrix[y][x]
        if reset:
            self.matrix[y][x] = 0
        
        if not(0 <= y-1 < self.height) or not(0 <= x + direciton < self.width):
            return False
        
        if random.random() > self.chance_to_disappear:
            new_value = max(value - self.temperature_loss, 0)
            self.matrix[y-1][x+direciton] = new_value
    
    def display(self):
        print("\033[H", end="")  # move cursor para o topo (sem piscar)
        for row in self.matrix:
            for value in row:
                color = fire_color(value)
                rgb_print("■", color, end=" ")
            print()

            
fire_sim = FireSimulation(HEIGHT, WIDTH, TEMPERATURE_LOSS, CHANCE_TO_DISAPPEAR)
fire_sim.display()

clear()
while True:
    fire_sim.update()
    fire_sim.display()
    
    time.sleep(0.1)