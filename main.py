import random
import math
import os
import pickle
import pygame

screen = pygame.display.set_mode((1280, 720))
icon = pygame.image.load("snake_icon.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake !")
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
snake_body_original = pygame.image.load("snake_body.png").convert_alpha()
snake_bottom_original = pygame.image.load("snake_bottom.png").convert_alpha()
img_fin = pygame.image.load("game_over.png").convert_alpha()
img_fin = pygame.transform.scale(img_fin, (1280, 720))
timer = 0
patates = []
points = 0

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))


def affichage(screen2: pygame.Surface, text: str, rect: object = (0, 0), _font: str = "Verdana", size: int = 6,
              color: tuple = (238, 244, 247)) -> None:
    font = pygame.font.SysFont(_font, size)
    text_img = font.render(text, True, color)
    screen2.blit(text_img, rect)


def affichage2(screen3: pygame.Surface, text: str, rect=(0, 0), _font: str = "Verdana", size: int = 6,
               color: tuple = (216, 0, 0)):
    font = pygame.font.SysFont(_font, size)
    text_img = font.render(text, True, color)
    screen3.blit(text_img, rect)


def fin():
    pygame.quit()
    quit()


def add_patate():
    global menu_fin
    global menu_error
    if points == 100:
        menu_error = True

    else:
        patates.append(Patate())
        if points > 0:  # ne fais pas crash lors de l'ajout de la patate initiale
            to_add_2 = corps[points + 3]
            to_add_2.show = True
            to_add_2.is_bottom = False
            to_add_2.original_image = pygame.transform.rotate(snake_body_original, 90)
            __direction = historique[points + 3].direction
            if __direction == Directions.RIGHT:
                to_add_2.image = pygame.transform.rotate(to_add_2.original_image, 0)
            elif __direction == Directions.LEFT:
                to_add_2.image = pygame.transform.rotate(to_add_2.original_image, 180)
            elif __direction == Directions.UP:
                to_add_2.image = pygame.transform.rotate(to_add_2.original_image, 90)
            elif __direction == Directions.DOWN:
                to_add_2.image = pygame.transform.rotate(to_add_2.original_image, -90)
            to_add = corps[points + 4]
            body_group.add(to_add)
            to_add.show = True
            to_add.is_bottom = True
            to_add.original_image = pygame.transform.rotate(snake_bottom_original, 90)
            __direction = historique[points + 4].direction
            if __direction == Directions.RIGHT:
                to_add.image = pygame.transform.rotate(to_add.original_image, 0)
            elif __direction == Directions.LEFT:
                to_add.image = pygame.transform.rotate(to_add.original_image, 180)
            elif __direction == Directions.UP:
                to_add.image = pygame.transform.rotate(to_add.original_image, 90)
            elif __direction == Directions.DOWN:
                to_add.image = pygame.transform.rotate(to_add.original_image, -90)


def update_patates():
    global points
    for patatoide in patates:
        patatoide.update()
        if patatoide.location.get_grid_pos() == snake_location.get_grid_pos():
            if not patatoide.eated:
                patatoide.eat()
                points = points + 1
                add_patate()
                # if random.randint(0, 10) > 9:
                #     add_patate()  # petite chance d'en voir une deuxième !


class Patate(pygame.sprite.Sprite):
    def __init__(self):
        super(Patate, self).__init__()
        self.image = patate
        self.location = Location(pygame.rect.Rect(0, 0, 20, 20))
        self.location.set_grid_pos((random.randint(1, 63), random.randint(1, 35)))
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


class Body(pygame.sprite.Sprite):
    def __init__(self, location: Location, _dir: str, is_bottom=False):
        super(Body, self).__init__()
        self.rect = pygame.rect.Rect(-1, -1, 20, 20)
        self.rect.x, self.rect.y = location.get_pos()
        self.location = Location(self.rect)
        self.original_image = pygame.transform.rotate(snake_body_original, 90)
        self.is_bottom = is_bottom
        self.direction = _dir
        self.cur_dir = self.direction
        self.show = True

        if self.is_bottom:
            self.original_image = pygame.transform.rotate(snake_bottom_original, 90)

        self.image = self.original_image

    def update_rect_from_location(self):
        self.rect.x, self.rect.y = self.location.get_pos()

    def update(self, index: int):
        self.direction = historique[index].direction
        if self.direction != self.cur_dir:
            not_equal = True
        else:
            not_equal = False
        if self.direction == Directions.RIGHT:
            self.rect.move_ip(1, 0)
            if not_equal:
                self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.direction == Directions.LEFT:
            self.rect.move_ip(-1, 0)
            if not_equal:
                self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == Directions.UP:
            self.rect.move_ip(0, -1)
            if not_equal:
                self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == Directions.DOWN:
            self.rect.move_ip(0, 1)
            if not_equal:
                self.image = pygame.transform.rotate(self.original_image, -90)
        if not_equal:
            self.cur_dir = self.direction
        tmp_rect = self.rect.copy()
        tmp_rect.x = self.rect.x + 2
        if self.show:
            screen.blit(self.image, tmp_rect)


class History:
    def __init__(self, _direction: str):
        super(History, self).__init__()
        self.direction = _direction

    def __str__(self):
        return "<History(Directions.%s)>" % self.direction.upper()

    def __repr__(self):
        return self.__str__()


def get_opposite(direct: str):
    """
    :type direct : str
    Fonction qui permet d'obtenir l'opposé d'une direction
    exemple : get_opposite(Directions.UP) renvoie l'opposé de UP : DOWN
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
    UP = "up"  # CONSTANTS
    RIGHT = "right"
    LEFT = "left"
    DOWN = "down"

    def __init__(self):
        super().__init__()


def sauvegarder(score):
    with open("sauvegarde.dat", "wb+") as file:
        pickle.dump(score, file)
        file.close()


def charger():
    with open("sauvegarde.dat", "rb") as file:
        save_data = pickle.load(file)
        file.close()
    return save_data


direction = Directions.RIGHT
current_direction = direction
add_patate()
snake_location = Location(pygame.rect.Rect(0, 0, 20, 20))
historique = [History(Directions.RIGHT) for x in range(0, 102)]
corps = []
boost_time_to_wait = 1000  # Le temps à attendre avant que le joueur peut denouveau se boost.
boost = boost_time_to_wait  # Le joueur peut se boost dès le début du jeu
boost_time_boosting = 250  # Détermine combien de temps le joueur est boost
body_group = pygame.sprite.Group()
menu_fin = False
menu_error = False
done_save = False


def jeux():
    global done_save
    global timer
    global patates
    global points
    global direction
    global current_direction
    global snake_location
    global historique
    global corps
    global boost_time_to_wait
    global boost
    global boost_time_boosting
    global body_group
    global menu_fin
    global menu_error
    global snake_head
    global snake_rect
    done_save = False
    snake_rect = pygame.Rect((1, -1), (20, 20))
    timer = 0
    patates = []
    points = 0
    if not os.path.isfile("sauvegarde.dat"):
        sauvegarder(0)  # Crée un fichier indiquant que le meilleur score est 0
    best_score = charger()
    print(best_score)

    direction = Directions.RIGHT
    current_direction = direction
    add_patate()
    snake_location = Location(pygame.rect.Rect(0, 0, 20, 20))
    historique = [History(Directions.RIGHT) for _ in range(0, 102)]
    corps = []
    boost_time_to_wait = 1000  # Le temps à attendre avant que le joueur peut de nouveau se booste.
    boost = boost_time_to_wait  # Le joueur peut se booste dès le début du jeu
    boost_time_boosting = 250  # Détermine combien de temps le joueur est boost
    body_group = pygame.sprite.Group()
    for _x in range(0, 300):
        corps.append(Body(Location(pygame.rect.Rect(-1 - _x * 20 - 20, -1, 20, 20)), Directions.RIGHT))

        if _x > 4:
            corps[_x].show = False
        else:
            body_group.add(corps[_x])
    corps[4] = Body(Location(pygame.rect.Rect(-1 - 100, -1, 20, 20)), Directions.RIGHT, True)  # Last is bottom :/

    menu_fin = False
    menu_error = False

    while True:
        if menu_fin:
            clock.tick(FPS)
            if not done_save:
                done_save = True
                try:
                    if points > best_score:
                        sauvegarder(points)
                except:
                    pass
            screen.blit(img_fin, (0, 0))
            _str = "Tu as mangé %s patate" % points
            if not points == 1:
                _str = _str + "s"
            affichage(screen, _str + " ! (Meilleur avant : %s)" % best_score, (200, 425), "Verdana", 40)
            affichage(screen, "Veux-tu recommencer la partie ?", (350, 500), "Verdana", 40)
            affichage(screen, "Appuie sur Entrée pour recommencer", (280, 550), "Verdana", 40)
            affichage(screen, "et sur Echap pour quitter.", (390, 600), "Verdana", 40)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        fin()
                    elif event.key == pygame.K_RETURN:
                        menu_fin = False
                        jeux()

        elif menu_error:
            clock.tick(FPS)
            affichage2(screen, "ERROR !", (350, 220), "Verdana", 150)
            pygame.display.update()

        else:
            clock.tick(FPS)
            if boost < boost_time_to_wait:
                boost += 1
            if boost < 0:
                factor = 2
            else:
                factor = 1
            for _iterator in range(0, factor):
                timer += 1
                if timer > 19:
                    snake_location.set_pos((snake_rect.x, snake_rect.y))
                    snake_location.set_grid_pos(
                        (snake_location.get_grid_pos()[0], snake_location.get_grid_pos()[1] + 1))  # le +
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
                    a = len(historique)
                    for x in range(0, a + 1):
                        historique[a - x - 1] = historique[a - x - 2]
                    historique[0] = (History(current_direction))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu_fin = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z or event.key == pygame.K_UP:
                            direction = Directions.UP
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            direction = Directions.DOWN
                        elif event.key == pygame.K_q or event.key == pygame.K_LEFT:
                            direction = Directions.LEFT
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            direction = Directions.RIGHT
                        elif event.key == pygame.K_SPACE:
                            if boost == boost_time_to_wait:
                                boost = boost_time_boosting * -1

                if current_direction == Directions.RIGHT:
                    snake_rect.move_ip(1, 0)
                elif current_direction == Directions.LEFT:
                    snake_rect.move_ip(-1, 0)
                elif current_direction == Directions.UP:
                    snake_rect.move_ip(0, -1)
                elif current_direction == Directions.DOWN:
                    snake_rect.move_ip(0, 1)
                screen.blit(img_grille, (0, 0))
                update_patates()
                for x in range(0, len(corps)):
                    try:
                        corps[x].update(x + 1)
                    except:
                        pass
                screen.blit(snake_head, snake_rect)
                pygame.display.update()
                if len(pygame.sprite.spritecollide(corps[0], body_group, False)) > 2:
                    menu_fin = True
                if (snake_location.get_grid_pos()[1] == 36) or (snake_location.get_grid_pos()[0] == 64) or \
                        (snake_location.get_grid_pos()[0] == -1) or (snake_location.get_grid_pos()[1] == -1):
                    menu_fin = True


jeux()
