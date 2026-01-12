import random
import pygame

FPS_LIMIT = 30
WIDTH = 500
HEIGHT = 400

CELL_SIZE = 4
NATURAL_DECAY = 8
PROPAGATION_DECAY = 12
PROPAGATION_DECAY_CHANCE = 0.25
WIND_FORCE = (3, 1)
MAX_VALUE = 255

ROWS = HEIGHT // CELL_SIZE
COLUMNS = WIDTH // CELL_SIZE

FIRE_PALETTE = [
    (0, 0, 0), # BLACK
    (195, 47, 39), # RED
    (250, 153, 20), # ORANGE
    (250, 188, 42), # YELLOW
    (255, 255, 255), # WHITE
]

def get_palette_color(palette, value):
    value = min(max(value, 0), 1)
    
    palette_last_index = len(palette) - 1
    
    palette_pos = palette_last_index * value
    palette_min = min(int(palette_pos), palette_last_index - 1)
    palette_max = min(palette_min + 1, palette_last_index)
    
    dif_min = palette_pos - palette_min
    dif_max = palette_max - palette_pos
    force_min = 1 - dif_min
    force_max = 1 - dif_max
    
    color_min = palette[palette_min]
    color_max = palette[palette_max]
    
    new_r = color_min[0] * force_min + color_max[0] * force_max
    new_g = color_min[1] * force_min + color_max[1] * force_max
    new_b = color_min[2] * force_min + color_max[2] * force_max
    new_color = (new_r, new_g, new_b)
    
    return new_color

class FireSimulation:
    def __init__(self, rows, columns, max_value, cell_size, natural_decay, propagation_decay, propagation_decay_chance, wind_force):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        
        self.natural_decay = natural_decay
        self.propagation_decay = propagation_decay
        self.propagation_decay_chance = propagation_decay_chance
        self.max_value = max_value
        self.wind_left = wind_force[0]
        self.wind_right = wind_force[1]
        
        self.matrix = self.get_initial_matrix()
        
        self.surface = pygame.Surface((self.columns * self.cell_size, self.rows * self.cell_size))
        
    def get_initial_matrix(self):
        initial_matrix = [
            [0 for _ in range(self.columns)] for _ in range(self.rows - 1)
        ]
        
        last_row = [self.max_value for _ in range(self.columns)]
        initial_matrix.append(last_row)
        return initial_matrix
    
    def update(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.fire_propagation(x, y)
                
    def fire_propagation(self, x, y):        
        # New position
        next_y = y - 1
        next_x = (x + random.randint(-self.wind_left, self.wind_right)) % self.columns
        
        # Propagation
        value = self.matrix[y][x]
        if 0 <= next_y < self.rows and value >= 0:
            decay_factor = 0
            if random.random() < self.propagation_decay_chance:
                decay_factor = 1
            
            self.matrix[next_y][next_x] = value - self.propagation_decay * decay_factor
        
        # Cooling
        self.matrix[y][x] = max(self.matrix[y][x] - self.natural_decay, 0)
        if y == self.rows - 1:
            self.matrix[y][x] = self.max_value
    
    def render(self):
        self.surface.fill((0, 0, 0))
        
        for y in range(self.rows):
            for x in range(self.columns):
                value = self.matrix[y][x]
                if value > 0:
                    color = get_palette_color(FIRE_PALETTE, value / self.max_value)
                    pygame.draw.rect(
                        self.surface, 
                        color, 
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    )
        
        return self.surface
        
class App:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.entities = []
    
    def main_loop(self, fps=30):
        self.running = True
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(fps)
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        for entity in self.entities:
            entity.update()
        
    def draw(self):
        screen = self.screen
        
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, (200, 0, 0), (400, 0, 50, 50))
        
        for entity in self.entities:
            entity_render = entity.render()
            screen.blit(entity_render, (0, 0))
            
        
        pygame.display.set_caption(f"FPS: {self.clock.get_fps():.0f}")
        pygame.display.flip()
    
    def add_entity(self, entity):
        self.entities.append(entity)
        

def main():
    pygame.init()
    
    app = App(WIDTH, HEIGHT)
    fire_sim = FireSimulation(ROWS, COLUMNS, MAX_VALUE, CELL_SIZE, NATURAL_DECAY, PROPAGATION_DECAY, PROPAGATION_DECAY_CHANCE, WIND_FORCE)
    app.add_entity(fire_sim)
    
    app.main_loop(FPS_LIMIT)

if __name__ == "__main__":
    main()