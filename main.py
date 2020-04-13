import pygame
import os

pygame.init()
winh = 500
winw = winh
win = pygame.display.set_mode((winw, winh))
ground_texture = pygame.image.load(os.path.join("src", "ground.png"))
mario_texture = pygame.image.load(os.path.join("src", "mario.png"))

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
        self, x, y, w, h, color, texture, g, x_vel, y_vel, x_max_vel, y_max_vel,  jump_height
    ):
        Rectangle.__init__(self, x, y, w, h, color, texture)
        self.g =g 
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

            

        



    def check_gravity_collide(self, rect, pipes):
        is_on_something = False
        if (self.y + self.h >= rect.y and self.y + self.h <= rect.y + rect.h )  :
            is_on_something = True
        
        for pipe in pipes:
            if (self.y + self.h >= pipe.y and self.y + self.h <= pipe.y + pipe.h and self.x + self.w >= pipe.x and self.x + self.w <= pipe.x + pipe.w):
                is_on_something = True
        return is_on_something

    def is_enity_above_too_low(self, pipes):
        for entity in pipes:
            if player.y - self.total_jump_height  > entity.y + entity.h and (self.x + self.w >= entity.x and self.x + self.w <= entity.x + entity.w):
                # enitiy is above
                
                return True
        return False

    def allow_jump(self, ground, pipes):
        allow_jump = False
        if self.check_gravity_collide( ground, pipes) and not(self.is_enity_above_too_low(pipes)):
            allow_jump = True

        return allow_jump

    def update(self, ground, pipes):
        print(self.y_vel)
        # if going to fall through, dont

        allow_y_vel = False
        
        #if legs are below pipe top and above pipe bottom
        for pipe in pipes:
            if (self.y + self.y_vel + self.h > pipe.y) and (self.y + self.y_vel + self.h < pipe.y + pipe.h)  and (self.x + self.w >= pipe.x and self.x <= pipe.x + pipe.w):
                allow_y_vel = False
                self.y += pipe.y - (self.y + self.h)
                self.y_vel = 0

        #ground collsion doesnt require x checking
        if self.y + self.y_vel + self.h < ground.y :
            allow_y_vel = True
        else:
            self.y += ground.y - (self.y + self.h)
            self.y_vel = 0
            allow_y_vel = False


        #pipe checking DOES require x checking
        #print("----")
        #print(self.x > pipe.x and self.x < pipe.x + pipe.w)
        #print((self.y + self.y_vel + self.h < pipe.y))

        #dont allow one round of gravity if it will make u get stuck in pipe
        # stuck in pipe means head is below pipe and legs are in pipe


        
            
        

        #print(allow_y_vel)
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
            self.x_vel -= 1
        elif self.x_vel < 0:
            self.x_vel += 1


ground = Rectangle(0, 450, 500, 50, [0, 255, 0], ground_texture)
player = Player(100, 50, 20, 30, [255, 0, 0], mario_texture, world_gravity,0, 0, 5, 5, 20)
pipe = Rectangle(100, 390, 100, 20, [0, 255, 0], None)
pipes = []


for i in range(0,5):
    y = i * 90 + 40
    
    pipes.append(Rectangle(100, y, 100, 20, [0, 255, 0], None))

pipes.append(Rectangle(250, 140, 50, 200, [0, 255, 0], None))

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
        pygame.draw.rect(win, piped.color, [piped.x, piped.y, piped.w, piped.h], 0)
        

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
        if player.allow_jump(ground, pipes):
            player.y_vel = player.jump_height
    # run update after key recog
    update()
    draw()


pygame.quit()
