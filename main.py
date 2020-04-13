import pygame as pygame
import os

pygame.init()
winh = 500
winw = winh
win = pygame.display.set_mode((winw, winh))
ground_texture = pygame.image.load(os.path.join("src", "ground.png"))
mario_texture = pygame.image.load(os.path.join("src", "mario.png"))
pipe_texture = pygame.image.load(os.path.join("src", "pipe.png"))
pygame.display.set_caption("Selest")

world_gravity = 2
max_gravity = 15


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
        self,
        x,
        y,
        w,
        h,
        color,
        texture,
        g,
        x_vel,
        y_vel,
        x_max_vel,
        y_max_vel,
        jump_height,
        friction,
    ):
        Rectangle.__init__(self, x, y, w, h, color, texture)
        self.g = g
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_max_vel = x_max_vel
        self.y_max_vel = y_max_vel
        self.jump_height = jump_height * -1

        test_vel = self.jump_height
        self.total_jump_height = 0
        while test_vel < 0:
            self.total_jump_height += test_vel

            # speed gravity up as heigh increases
            if test_vel + self.g < max_gravity:

                test_vel = test_vel + world_gravity

        self.friction = friction
        x_max_test_vel = self.x_max_vel
        self.total_x_movement = 0
        while x_max_test_vel > 0:
            self.total_x_movement += x_max_test_vel
            x_max_test_vel -= self.friction

        print(self.total_x_movement)

    def check_gravity_collide(self, rect, pipes):
        is_on_something = False
        if self.y + self.h >= rect.y and self.y + self.h <= rect.y + rect.h:
            is_on_something = True

        for pipe in pipes:
            if (
                self.y + self.h >= pipe.y
                and self.y + self.h <= pipe.y + pipe.h
                and self.x + self.w >= pipe.x
                and self.x + self.w <= pipe.x + pipe.w
            ):
                is_on_something = True
        return is_on_something

    def is_enity_above_too_low(self, pipes):
        for entity in pipes:
            if player.y - self.total_jump_height < entity.y + entity.h and (
                self.x + self.w > entity.x and self.x + self.w < entity.x + entity.w
            ):
                # enitiy is above
                print(entity.y, entity.h, entity.x)
                print(player.y - self.total_jump_height)

                return True
        return False

    def allow_jump(self, ground, pipes):
        allow_jump = False
        print(self.check_gravity_collide(ground, pipes))
        print(not (self.is_enity_above_too_low(pipes)))
        if self.check_gravity_collide(ground, pipes) and not (
            self.is_enity_above_too_low(pipes)
        ):
            allow_jump = True

        return allow_jump

    def update(self, ground, pipes):

        # if going to fall through, dont

        allow_y_vel = False

        # if legs are below pipe top and above pipe bottom
        for pipe in pipes:
            # if going the velociy will make u go through the entity, just teloport to the entity top (make it seem like u hit the ground and stopped)
            if (
                (self.y + self.y_vel + self.h > pipe.y)
                and (self.y + self.y_vel + self.h < pipe.y + pipe.h)
                and (self.x + self.w >= pipe.x and self.x <= pipe.x + pipe.w)
            ):
                allow_y_vel = False
                self.y += pipe.y - (self.y + self.h)
                self.y_vel = 0

        # ground collsion doesnt require x checking
        # if going the velociy will make u go through the ground top, just teloport to the ground (make it seem like u hit the ground and stopped)
        if self.y + self.y_vel + self.h < ground.y:
            allow_y_vel = True
        else:
            self.y += ground.y - (self.y + self.h)
            self.y_vel = 0
            allow_y_vel = False

        if allow_y_vel:
            self.y += self.y_vel

        self.x += self.x_vel

        # add friction
        """
        if self.y_vel > 0:
            self.y_vel -= 1
        elif self.y_vel < 0:
            self.y_vel += 1
        """

        if self.x_vel > 0:
            self.x_vel -= self.friction
        elif self.x_vel < 0:
            self.x_vel += self.friction

    def allow_right_move(self, entities):
        # print(entities[-1].x)
        allow = True
        for entity in entities:
            print(self.total_x_movement)

            # if on the players right move the playere will be inside eniity, DONT MOVE
            if self.x + self.w + self.total_x_movement >= entity.x:

                # check if feet will be inside entity
                # if head inside or feet inside
                if (self.y > entity.y and self.y < entity.y + entity.h) or (
                    self.y + self.h > entity.y and self.y + self.h < entity.y + entity.h
                ):
                    allow = False
                    self.x_vel = 0

                    # to teloport (sharply)
                    self.x += entity.x - self.x - self.w - 1
                    # comment out to stop early

        return allow


ground = Rectangle(0, 450, 500, 50, [0, 255, 0], ground_texture)
player = Player(
    100, 50, 20, 30, [255, 0, 0], mario_texture, world_gravity, 0, 0, 6, 5, 20, 1
)

pipes = []


class ViewObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y


camera = ViewObject(200, 0)

for i in range(0, 5):
    x = i * 90 + 100

    pipes.append(Rectangle(x, 100, 50, 50, [0, 255, 0], pipe_texture))

pipes.append(Rectangle(250, 300, 50, 200, [0, 255, 0], pipe_texture))


def update():
    player.update(ground, pipes)

    # add one round of graviy to check if you will fall through

    # player.y += player.y_vel

    if player.check_gravity_collide(ground, pipes):

        player.y_vel = 0
    else:
        if player.y_vel + player.g < max_gravity:

            player.y_vel = player.y_vel + world_gravity


def draw():

    win.fill([146, 144, 255])

    # pygame.draw.rect(win, ground.color, [ground.x, ground.y, ground.w, ground.h], 0)
    char = pygame.transform.scale(ground.texture, (ground.w, ground.h))
    win.blit(char, (ground.x, ground.y))

    # pygame.draw.rect(win, player.color, [player.x, player.y, player.w, player.h], 0)
    char = pygame.transform.scale(player.texture, (player.w, player.h))
    win.blit(char, (player.x, player.y))

    for piped in pipes:
        # pygame.draw.rect(win, piped.color, [piped.x, piped.y, piped.w, piped.h], 0)
        char = pygame.transform.scale(piped.texture, (piped.w, piped.h))
        win.blit(char, (piped.x, piped.y))

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

        # print(player.allow_right_move(pipes))
        # 15 is the total amount moved
        if player.allow_right_move(pipes):
            if player.x_vel < player.x_max_vel:
                player.x_vel = player.x_max_vel
    if keys[pygame.K_LEFT]:
        # 15 is the total amount moved
        if player.x_vel > -player.x_max_vel:
            player.x_vel = -player.x_max_vel
    if keys[pygame.K_UP]:

        # print(player.allow_jump(ground, pipes))
        if player.allow_jump(ground, pipes):
            player.y_vel = player.jump_height
    # run update after key recog
    update()
    draw()


pygame.quit()
