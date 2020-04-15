import pygame as pygame
import os

pygame.init()
winh = 500
winw = winh
win = pygame.display.set_mode((winw, winh))
ground_texture = pygame.image.load(os.path.join("src", "ground.png"))
mario_texture = pygame.image.load(os.path.join("src", "mario.png"))
mario_texture_two = pygame.transform.flip(
    pygame.image.load(os.path.join("src", "mario.png")), True, False
)
pipe_texture = pygame.image.load(os.path.join("src", "pipe.png"))
lucky_texture = pygame.image.load(os.path.join("src", "lucky.png"))


pygame.display.set_caption("Selest")

world_gravity = 2
max_gravity = 15


class Rectangle:
    def __init__(self, x, y, w, h, color, texture, type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.texture = texture
        self.type = type


class Player(Rectangle):
    def __init__(
        self,
        x,
        y,
        w,
        h,
        color,
        texture,
        type,
        g,
        x_vel,
        y_vel,
        x_max_vel,
        y_max_vel,
        jump_height,
        friction,
    ):
        Rectangle.__init__(self, x, y, w, h, color, texture, type)
        self.g = g
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_max_vel = x_max_vel
        self.y_max_vel = y_max_vel
        self.jump_height = jump_height * -1
        self.clicked_jump = False

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

    def check_gravity_collide(self, rect, entities):
        is_on_something = False
        if self.y + self.h >= rect.y and self.y + self.h <= rect.y + rect.h:
            is_on_something = True

        for entity in entities:
            if (
                self.y + self.h >= entity.y
                and self.y + self.h <= entity.y + entity.h
                and self.x + self.w >= entity.x
                and self.x <= entity.x + entity.w
            ):
                is_on_something = True
        return is_on_something

    def is_enity_above_too_low(self, entities):

        for entity in entities:
            # enitiy is above

            if (
                self.y + self.total_jump_height < entity.y + entity.h
                and self.y + self.h > entity.y
                and (self.x + self.w > entity.x and self.x < entity.x + entity.w)
            ):

                # you are allowed to jump into lucky blocks so you allow to phase if luycy
                if entity.type != "lucky":

                    return True
        return False

    def allow_jump(self, ground, entities):
        allow_jump = False

        if self.check_gravity_collide(ground, entities) and not (
            self.is_enity_above_too_low(entities)
        ):
            allow_jump = True

        return allow_jump

    def update(self, ground, entities):

        # if going to fall through, dont

        allow_y_vel = False

        # if legs are below pipe top and above pipe bottom
        for entity in entities:
            # if going the velociy will make u go through the entity, just teloport to the entity top (make it seem like u hit the ground and stopped)
            if (self.y + self.y_vel + self.h > entity.y) and (
                self.y + self.y_vel + self.h < entity.y + entity.h
            ):
                if self.x + self.w > entity.x and self.x < entity.x + entity.w:
                    # only tp to top if moving down
                    if self.y_vel > 0:
                        allow_y_vel = False
                        self.y += entity.y - (self.y + self.h)
                        self.y_vel = 0

                    elif self.y_vel < 0:  # if moving up

                        if entity.type == "lucky":
                            self.y = entity.y + entity.h
                            self.y_vel = 20

                # if moving left into entity, check if u will move into it

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

        # friction as to not slide off the map
        if self.x_vel > 0:
            self.x_vel -= self.friction
        elif self.x_vel < 0:
            self.x_vel += self.friction

    def allow_right_move(self, entities):
        # print(entities[-1].x)
        allow = True
        for entity in entities:

            # if on the players right move the playere will be inside eniity, DONT MOVE
            if (
                self.x + self.w + self.total_x_movement >= entity.x
                and self.x + self.w + self.total_x_movement <= entity.x + entity.w
            ):

                # check if feet will be inside entity
                # if head inside or feet inside
                if (self.y > entity.y and self.y < entity.y + entity.h) or (
                    self.y + self.h > entity.y and self.y + self.h < entity.y + entity.h
                ):
                    allow = False
                    self.x_vel = 0

                    # to teloport (sharply)
                    self.x += entity.x - self.x - self.w - 5
                    # comment out to stop early

        return allow

    def allow_left_move(self, entities):
        # print("Allow left move")
        # print(entities[-1].x)
        allow = True
        for entity in entities:

            # if on the players right move the playere will be inside eniity, DONT MOVE
            if (
                self.x + -self.total_x_movement <= entity.x + entity.w
                and self.x + self.w - self.total_x_movement >= entity.x
            ):

                # check if feet will be inside entity
                # if head inside or feet inside
                if (self.y > entity.y and self.y < entity.y + entity.h) or (
                    self.y + self.h > entity.y and self.y + self.h < entity.y + entity.h
                ):

                    allow = False
                    self.x_vel = 0

                    # to teloport (sharply)
                    self.x = entity.x + entity.w + 3
                    # comment out to stop early

        return allow


ground = Rectangle(0, 450, 500, 50, [0, 255, 0], ground_texture, "ground")
player = Player(
    100,
    50,
    20,
    30,
    [255, 0, 0],
    mario_texture,
    "player",
    world_gravity,
    0,
    0,
    6,
    5,
    20,
    1,
)

entities = []


class ViewObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y


camera = ViewObject(200, 0)
"""
for i in range(0, 2):
    x = i * 110 + 100

    entities.append(Rectangle(x, 100, 50, 50, [0, 255, 0], pipe_texture, "pipe"))
"""
entities.append(Rectangle(250, 400, 50, 200, [0, 255, 0], pipe_texture, "pipe"))
entities.append(Rectangle(250, 300, 50, 50, [0, 255, 0], pipe_texture, "pipe"))

entities.append(Rectangle(100, 350, 25, 25, [0, 255, 0], lucky_texture, "lucky"))


def update():

    player.update(ground, entities)

    # add one round of graviy to check if you will fall through

    # player.y += player.y_vel

    if player.check_gravity_collide(ground, entities):

        player.y_vel = 0
    else:
        if player.y_vel + player.g < max_gravity:

            player.y_vel = player.y_vel + world_gravity


def draw():

    win.fill([146, 144, 255])

    # draw background grids

    # for dev grid
    """
    for index in range(0, winw, 25):
        pygame.draw.line(win, (0, 0, 0), (index, 0), (index, winh), 1)
    """

    # pygame.draw.rect(win, ground.color, [ground.x, ground.y, ground.w, ground.h], 0)
    char = pygame.transform.scale(ground.texture, (ground.w, ground.h))
    win.blit(char, (ground.x, ground.y))

    # pygame.draw.rect(win, player.color, [player.x, player.y, player.w, player.h], 0)
    char = pygame.transform.scale(player.texture, (player.w, player.h))
    win.blit(char, (player.x, player.y))

    for entity in entities:
        # pygame.draw.rect(win, entity.color, [entity.x, entity.y, entity.w, entity.h], 0)
        char = pygame.transform.scale(entity.texture, (entity.w, entity.h))
        win.blit(char, (entity.x, entity.y))

    pygame.display.update()


clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():

        # check if window was losed to stop the game loop
        if event.type == pygame.QUIT:
            run = False

    player.clicked_jump = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        # print("jump clicked")

        if player.allow_jump(ground, entities):
            player.clicked_jump = True
            player.y_vel = player.jump_height
    if keys[pygame.K_RIGHT]:

        # print(player.allow_right_move(pipes))
        # 15 is the total amount moved
        if player.allow_right_move(entities):
            if player.x_vel < player.x_max_vel:
                player.x_vel = player.x_max_vel
    if keys[pygame.K_LEFT]:
        # 15 is the total amount moved
        # print(player.allow_left_move(entities))
        if player.allow_left_move(entities):
            if player.x_vel > -player.x_max_vel + -4:
                player.x_vel = -player.x_max_vel

    # run update after key recog
    update()
    draw()


pygame.quit()
