import pygame
import os

pygame.init()
winh = 500
winw = winh
win = pygame.display.set_mode((winw, winh))
ground_texture = pygame.image.load(os.path.join("src", "ground.png"))
mario_texture = pygame.image.load(os.path.join("src", "mario.png"))

pygame.display.set_caption("Selest")


class Rectangle:
    def __init__(self, x, y, w, h, color, texture):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.texture = texture


class Player(Rectangle):
    def __init__(
        self, x, y, w, h, color, texture, x_vel, y_vel, x_max_vel=0, y_max_vel=0
    ):
        Rectangle.__init__(self, x, y, w, h, color, texture)
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_max_vel = x_max_vel
        self.y_max_vel = y_max_vel

    def check_gravity_collide(self, rect):
        if self.y + self.h >= rect.y and self.y + self.h <= rect.y + rect.h:
            return True
        else:
            return False

    def update(self, ground):
        # if going to fall through, dont
        if self.y + self.y_vel + self.h < ground.y:
            self.y += self.y_vel
        else:
            self.y += ground.y - (self.y + self.h)
            self.y_vel = 0
        self.x += self.x_vel

        # add friction
        """
        if self.y_vel > 0:
            self.y_vel -= 1
        elif self.y_vel < 0:
            self.y_vel += 1
        """

        if self.x_vel > 0:
            self.x_vel -= 1
        elif self.x_vel < 0:
            self.x_vel += 1


ground = Rectangle(0, 450, 500, 50, [0, 255, 0], ground_texture)
player = Player(100, 50, 20, 30, [255, 0, 0], mario_texture, 0, 0, 5, 5)


def update():
    player.update(ground)

    # add one round of graviy to check if you will fall through
    amnt = 2
    # player.y += player.y_vel

    if player.check_gravity_collide(ground):

        player.y_vel = 0
    else:
        if player.y_vel + amnt < 10:

            player.y_vel = player.y_vel + amnt


def draw():

    win.fill([146, 144, 255])

    # pygame.draw.rect(win, ground.color, [ground.x, ground.y, ground.w, ground.h], 0)
    char = pygame.transform.scale(ground.texture, (ground.w, ground.h))
    win.blit(char, (ground.x, ground.y))

    # pygame.draw.rect(win, player.color, [player.x, player.y, player.w, player.h], 0)
    char = pygame.transform.scale(player.texture, (player.w, player.h))
    win.blit(char, (player.x, player.y))

    pygame.display.update()


clock = pygame.time.Clock()

run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():

        # check if window was losed to stop the game loop
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        # 15 is the total amount moved
        if player.x_vel <= 4:
            player.x_vel += 4
    if keys[pygame.K_LEFT]:
        # 15 is the total amount moved
        if player.x_vel >= -4:
            player.x_vel += -4
    if keys[pygame.K_UP]:
        player.y_vel = -10
    # run update after key recog
    update()
    draw()


pygame.quit()
