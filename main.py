import random
import math
import pygame
import tkinter
import tkinter.messagebox

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
FPS = 120
img_grille = pygame.image.load("grille.png").convert_alpha()
patate = pygame.image.load("potato.png").convert_alpha()
patate = pygame.transform.scale(patate, (20, 20))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (100, 0, 100)

snake_rect = pygame.Rect((1, -1), (20, 20))
snake_head_original = pygame.image.load("snake_head.png").convert_alpha()
snake_head = pygame.transform.rotate(snake_head_original, 90)

timer = 0

patates = []

points = 0


def fin():
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo("Fin de la partie", "Vous avez mangé {0} patates".format(points))
    root.destroy()
    quit()


def add_patate():
    patates.append(Patate())


def update_patates():
    global points
    for patatoide in patates:
        patatoide.update()
        if patatoide.location.get_grid_pos() == snake_location.get_grid_pos():
            if not patatoide.eated:
                patatoide.eat()
                points = points + 1
                add_patate()
                if random.randint(0, 10) > 9:
                    add_patate()  # petite chance d'en voir une deuxième !


class Patate(pygame.sprite.Sprite):
    def __init__(self):
        super(Patate, self).__init__()
        self.image = patate
        self.location = Location(pygame.rect.Rect(0, 0, 20, 20))
        self.location.set_grid_pos((random.randint(0, 64), random.randint(0, 36)))
        self.rect = self.image.get_rect()
        self.rect.x = self.location.x
        self.rect.y = self.location.y
        self.eated = False

    def update(self):
        if not self.eated:
            screen.blit(self.image, self.rect)

    def eat(self):
        self.eated = True


class Location:
    def __init__(self, rect: pygame.rect.Rect):
        super(Location, self).__init__()
        self.grid_y = 0
        self.grid_x = 0
        self.x, self.y = rect.x, rect.y
        self.update_from_pos()

    def get_grid_pos(self):
        return self.grid_x, self.grid_y

    def update_from_pos(self):
        self.grid_x = int(math.floor(self.x / 20))
        self.grid_y = int(math.floor(self.y / 20))

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, pos):
        self.x, self.y = pos
        self.update_from_pos()

    def set_grid_pos(self, pos):
        self.grid_x, self.grid_y = int(pos[0]), int(pos[1])
        self.x, self.y = self.grid_x * 20, self.grid_y * 20


def get_opposite(direct: str):
    """
    :type direct: str
    Fonction qui permet d'obtenir l'opposé d'une direction
    exemple : get_opposite(Directions.UP) renvoie l'opposé de UP : self.DOWN
    """
    if direct == Directions.UP:
        return Directions.DOWN
    elif direct == Directions.DOWN:
        return Directions.UP
    elif direct == Directions.RIGHT:
        return Directions.LEFT
    elif direct == Directions.LEFT:
        return Directions.RIGHT
    return Directions.RIGHT


class Directions:
    UP = "up"
    RIGHT = "right"
    LEFT = "left"
    DOWN = "down"

    def __init__(self):
        super().__init__()


direction = Directions.RIGHT
current_direction = direction
add_patate()
snake_location = Location(pygame.rect.Rect(0, 0, 20, 20))

while True:
    clock.tick(FPS)
    timer += 1
    if timer > 19:
        snake_location.set_pos((snake_rect.x, snake_rect.y))
        snake_location.set_grid_pos((snake_location.get_grid_pos()[0], snake_location.get_grid_pos()[1] + 1))  # le +
        # 1 fix le bug de -1, fin laisse comme ça
        if not direction == get_opposite(current_direction):
            current_direction = direction
        if current_direction == Directions.RIGHT:
            snake_head = pygame.transform.rotate(snake_head_original, 90)
        elif current_direction == Directions.LEFT:
            snake_head = pygame.transform.rotate(snake_head_original, -90)
        elif current_direction == Directions.UP:
            snake_head = pygame.transform.rotate(snake_head_original, 180)
        elif current_direction == Directions.DOWN:
            snake_head = pygame.transform.rotate(snake_head_original, 0)
        timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                direction = Directions.UP
            elif event.key == pygame.K_s:
                direction = Directions.DOWN
            elif event.key == pygame.K_q:
                direction = Directions.LEFT
            elif event.key == pygame.K_d:
                direction = Directions.RIGHT

    if current_direction == Directions.RIGHT:
        snake_rect.move_ip(1, 0)
    elif current_direction == Directions.LEFT:
        snake_rect.move_ip(-1, 0)
    elif current_direction == Directions.UP:
        snake_rect.move_ip(0, -1)
    elif current_direction == Directions.DOWN:
        snake_rect.move_ip(0, 1)



    screen.blit(img_grille, (0, 0))
    # screen.blit(patate, (0, 0))
    update_patates()
    screen.blit(snake_head, snake_rect)
    pygame.display.update()
    if (snake_location.get_grid_pos()[1] == 36) or (snake_location.get_grid_pos()[0] == 64) or \
            (snake_location.get_grid_pos()[0] == -1) or (snake_location.get_grid_pos()[1] == -1):
        fin()
#test