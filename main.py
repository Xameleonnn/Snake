import pygame
import random
pygame.font.init()

class Cube:
    
    def __init__(self, colour, position, direction_x, direction_y, rect_cube = None):
        self.colour = colour
        self.position = position
        self.direction_x = direction_x
        self.direction_y = direction_y

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        step = WIDTH/ROWS
        self.position = (self.position[0] + self.direction_x * step, self.position[1] + self.direction_y * step)
        if self.position[0] == -WIDTH/ROWS:
            self.position = (WIDTH-WIDTH/ROWS, self.position[1])
        elif self.position[0] == WIDTH:
            self.position = (0, self.position[1])
        elif self.position[1] == -WIDTH/ROWS:
            self.position = (self.position[0], WIDTH-WIDTH/ROWS)
        elif self.position[1] == WIDTH:
            self.position = (self.position[0], 0)

    def draw_cube(self, head = False):
        row = self.position[0]
        column = self.position[1]
        size_of_cube = WIDTH//ROWS-2
        self.rect_cube = pygame.Rect(row+2, column+2, size_of_cube, size_of_cube)
        pygame.draw.rect(WINDOW, self.colour, (row+2, column+2, size_of_cube, size_of_cube))

        if head:
            centre = size_of_cube//2
            eye_1 = (row+ 2 + centre - centre//2, column+ 2 + size_of_cube//4)
            eye_2 = (row+ 2 + centre + centre//2, column+ 2 + size_of_cube//4)
            pygame.draw.circle(WINDOW, (0, 0, 0), eye_1, 5)
            pygame.draw.circle(WINDOW, (0, 0, 0), eye_2, 5)

    def set_direction(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y

    def get_direction(self):
        return (self.direction_x, self.direction_y)

    def get_rect(self): # for handling collision we need a rect object
        return self.rect_cube

class Snake:
    body = []
    turns = {} # for storing turns as tup(coordinates:direction)
    
    def __init__(self, SNAKE_COLOUR, position):
        self.colour = SNAKE_COLOUR
        self.position = position
        self.direction_x = 0
        self.direction_y = 1
        self.head = Cube(self.colour, self.position, self.direction_x, self.direction_y)
        self.body.append(self.head)
        
    
    def move(self, key_pressed):
        head_coords = (self.head.position[:]) # making a tuple, so we can store a list as key in dict
        if key_pressed[pygame.K_a]:
            self.direction_x = -1
            self.direction_y = 0
            self.turns[head_coords] = [self.direction_x, self.direction_y]

        if key_pressed[pygame.K_w]:
            self.direction_x = 0
            self.direction_y = -1
            self.turns[head_coords] = [self.direction_x, self.direction_y]

        if key_pressed[pygame.K_d]:
            self.direction_x = 1
            self.direction_y = 0
            self.turns[head_coords] = [self.direction_x, self.direction_y]

        if key_pressed[pygame.K_s]:
            self.direction_x = 0
            self.direction_y = 1
            self.turns[head_coords] = [self.direction_x, self.direction_y]
        
        for index, cube_object in enumerate(self.body): # handling proper movement of the body
            turns_copy = self.turns.copy()
            x, y = cube_object.get_direction()
            for key in turns_copy.keys():
                if cube_object.position[:] == key:
                    x, y = self.turns.get(cube_object.position[:]) # getting direction of the turn
                    cube_object.set_direction(x, y)

            for key in turns_copy.keys():
                if index == len(self.body) - 1 and cube_object.position[:] == key:
                    self.turns.pop(cube_object.position[:], None)
            
            cube_object.move(x, y)
    
    def reset(self):
        self.body.clear()
        self.turns.clear()
        self.position = (100,100)
        self.direction_x = 0
        self.direction_y = 1
        self.head = Cube(self.colour, self.position, self.direction_x, self.direction_y)
        self.body.append(self.head)
        draw_window()
        main()

    def add_cube(self):
        last_cube = self.body[-1]
        direction_last_cube = last_cube.get_direction()
        direction_last_cube_x, direction_last_cube_y = direction_last_cube
        if last_cube.direction_x == -1 and last_cube.direction_y == 0:
            self.body.append(Cube(SNAKE_COLOUR, (last_cube.position[0] + WIDTH/ROWS, last_cube.position[1]), direction_last_cube_x, direction_last_cube_y))
        if last_cube.direction_x == 0 and last_cube.direction_y == -1:
            self.body.append(Cube(SNAKE_COLOUR, (last_cube.position[0], last_cube.position[1] + WIDTH/ROWS), direction_last_cube_x, direction_last_cube_y))
        if last_cube.direction_x == 1 and last_cube.direction_y == 0:
            self.body.append(Cube(SNAKE_COLOUR, (last_cube.position[0] - WIDTH/ROWS, last_cube.position[1]), direction_last_cube_x, direction_last_cube_y))
        if last_cube.direction_x == 0 and last_cube.direction_y == 1:
            self.body.append(Cube(SNAKE_COLOUR, (last_cube.position[0], last_cube.position[1] - WIDTH/ROWS), direction_last_cube_x, direction_last_cube_y))
        
    def draw_snake(self):
        for index, cube_object in enumerate(self.body):
            if index == 0:
                cube_object.draw_cube(True)
            else:
                cube_object.draw_cube()

pygame.display.set_caption('Snake game')
WIDTH = 1000
ROWS = 20
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
BACKGROUND_COLOUR = (200, 210, 245)
BORDERLINE_COLOUR = (0, 0, 0)
SNAKE_COLOUR = (255,100,100)
FOOD_COLOUR = (50,255,100)
FPS = 10
SNAKE = Snake(SNAKE_COLOUR, (100,100))
FOOD_LIST = []

def draw_grid():
    row_width = WIDTH//ROWS
    x = 0
    y = 0
    for _ in range(0, ROWS):
        x = x + row_width
        pygame.draw.line(WINDOW, BORDERLINE_COLOUR, (x, 0), (x, WIDTH), 2)

    for _ in range(0, ROWS):
        y = y + row_width
        pygame.draw.line(WINDOW, BORDERLINE_COLOUR, (0, y), (WIDTH, y), 2)

def draw_window():
    WINDOW.fill((BACKGROUND_COLOUR))
    draw_grid()
    if len(FOOD_LIST) == 0:
        get_food(SNAKE)
    else:
        FOOD_LIST[0].draw_cube()

    SNAKE.draw_snake()
    pygame.display.update()

def get_food(SNAKE):
    search = True
    while search: # food should not spawn in the body
        random_position = (random.randrange(ROWS) * WIDTH/ROWS, random.randrange(ROWS) * WIDTH/ROWS)
        food = Cube(FOOD_COLOUR, random_position, 1, 0)
        food.draw_cube()
        SNAKE.draw_snake()
        for segment in SNAKE.body:
            if food.get_rect().colliderect(segment.get_rect()):
                break
            
            if segment == SNAKE.body[-1]:
                search = False
        
    FOOD_LIST.append(food)
        
def handle_food(FOOD_LIST): # handling collision of the snake and the food
    if len(FOOD_LIST) > 0:
        food = FOOD_LIST[0]
        if SNAKE.body[0].rect_cube.colliderect(food.get_rect()):
            FOOD_LIST.remove(food)
            SNAKE.add_cube()

def draw_message(message):
    message_font = pygame.font.SysFont('comicsans', 100)
    render_message = message_font.render(message, 1, (0, 0, 0))
    substrate_message = pygame.Rect(0, 0, WIDTH, WIDTH)
    pygame.draw.rect(WINDOW, BACKGROUND_COLOUR, substrate_message)
    WINDOW.blit(render_message, (WIDTH//2 - render_message.get_width()//2, WIDTH//2 - render_message.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        key_pressed = pygame.key.get_pressed()
        SNAKE.move(key_pressed)
        handle_food(FOOD_LIST)
        draw_window()
        if len(SNAKE.body) != 1: # Condition for ending the game
            for cube_num in range(1, len(SNAKE.body)): 
                rect_object = SNAKE.body[cube_num].get_rect()
                if SNAKE.body[0].rect_cube.colliderect(rect_object): # handling collision of the head with the body
                    run = False
                    score = len(SNAKE.body)
                    draw_message(f'Game over, your score is {score}')
                    SNAKE.reset()

if __name__ == '__main__':
    main()

