import pygame
import os
import random


pygame.init()
height = 600
width = 1100
screen = pygame.display.set_mode((width, height))

running_pic = [pygame.image.load(os.path.join('project/project/project pygamr', 'dinosaur_run_one.png')),
               pygame.image.load(os.path.join('project/project/project pygamr', 'dinosaur_run_two.png'))]
jumping_pic = pygame.image.load(
    os.path.join('project/project/project pygamr', 'dinosaur_jump.png'))
ducking_pic = [pygame.image.load(os.path.join('project/project/project pygamr', 'dinosaur_duck_one.png')),
               pygame.image.load(os.path.join('project/project/project pygamr', 'dinosaur_duck_one.png'))]
small_cactus_pic = [pygame.image.load(os.path.join('project/project/project pygamr', 'small_cactus_one.png')),
                    pygame.image.load(os.path.join(
                        'project/project/project pygamr', 'small_cactus_two.png')),
                    pygame.image.load(os.path.join('project/project/project pygamr', 'small_cactus_three.png'))]
big_cactus_pic = [pygame.image.load(os.path.join('project/project/project pygamr', 'big_cactus_one.png')),
                  pygame.image.load(os.path.join(
                      'project/project/project pygamr', 'big_cactus_two.png')),
                  pygame.image.load(os.path.join('project/project/project pygamr', 'big_cactus_three.png'))]
pterodactyl = [pygame.image.load(os.path.join('project/project/project pygamr', 'pterodactyl_one.png')),
               pygame.image.load(os.path.join('project/project/project pygamr', 'pterodactyl_two.png'))]
cloud = pygame.image.load(os.path.join(
    'project/project/project pygamr', 'cloud.png'))
ground = pygame.image.load(os.path.join(
    'project/project/project pygamr', 'ground.png'))

speed_of_game = 14


class Game:
    def __init__(self):
        self.running = True

        self.clock = pygame.time.Clock()
        self.player = Dinosaur()
        self.cloud = Cloud()

        self.position_x_two = 0
        self.position_y_two = 380
        self.points_of_player = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def score(self):
        global speed_of_game
        self.points_of_player += 1
        if not self.points_of_player % 250:
            speed_of_game += 1

        text = self.font.render(
            'Счёт: ' + str(self.points_of_player), True, (0, 0, 0))
        rectangle_of_text = text.get_rect()
        rectangle_of_text.center = (1000, 40)
        screen.blit(text, rectangle_of_text)

    def background(self):
        global speed_of_game
        image_width = ground.get_width()
        screen.blit(ground, (self.position_x_two, self.position_y_two))
        screen.blit(ground, (self.position_x_two +
                             image_width, self.position_y_two))

        if self.position_x_two <= -image_width:
            screen.blit(ground, (self.position_x_two +
                                 image_width, self.position_y_two))
            self.position_x_two = 0
        self.position_x_two -= speed_of_game

    def play(self):
        fps = 30
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((255, 255, 255))
            input_of_user = pygame.key.get_pressed()

            self.player.draw(screen)
            self.player.update(input_of_user)

            self.cloud.draw(screen)
            self.cloud.update()

            self.background()

            self.score()

            self.clock.tick(fps)
            pygame.display.update()


class Dinosaur:
    position_x = 80
    position_y = 310
    position_y_of_duck = 340
    jump_val_first = 8.5

    def __init__(self):
        self.duck_img = ducking_pic
        self.run_img = running_pic
        self.jump_img = jumping_pic

        self.dinosaur_duck = False
        self.dinosaur_run = True
        self.dinosaur_jump = False

        self.step_index = 0
        self.jump_val = self.jump_val_first
        self.image = self.run_img[0]
        self.dinosaur_rect = self.image.get_rect()
        self.dinosaur_rect.x = self.position_x
        self.dinosaur_rect.y = self.position_y

    def update(self, event):

        if self.dinosaur_duck:
            self.duck()
        if self.dinosaur_run:
            self.run()
        if self.dinosaur_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if event[pygame.K_UP] and not self.dinosaur_jump:
            self.dinosaur_duck = False
            self.dinosaur_run = False
            self.dinosaur_jump = True

        elif event[pygame.K_DOWN] and not self.dinosaur_jump:
            self.dinosaur_duck = True
            self.dinosaur_run = False
            self.dinosaur_jump = False

        elif not (self.dinosaur_jump or event[pygame.K_DOWN]):
            self.dinosaur_duck = False
            self.dinosaur_run = True
            self.dinosaur_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dinosaur_rect = self.image.get_rect()
        self.dinosaur_rect.x = self.position_x
        self.dinosaur_rect.y = self.position_y_of_duck
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dinosaur_rect = self.image.get_rect()
        self.dinosaur_rect.x = self.position_x
        self.dinosaur_rect.y = self.position_y
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dinosaur_jump:
            self.dinosaur_rect.y -= self.jump_val * 4
            self.jump_val -= 0.8
        if self.jump_val < - self.jump_val_first:
            self.dinosaur_jump = False
            self.jump_val = self.jump_val_first

    def draw(self, screen):
        screen.blit(self.image, (self.dinosaur_rect.x, self.dinosaur_rect.y))


class Cloud:
    def __init__(self):
        self.position_x_cloud = width + random.randint(800, 1000)
        self.position_y_cloud = random.randint(50, 100)
        self.image = cloud
        self.width = self.image.get_width()

    def update(self):
        global speed_of_game
        self.position_x_cloud -= speed_of_game
        if self.position_x_cloud < -self.width:
            self.position_x_cloud = width + random.randint(2500, 3000)
            self.position_y_cloud = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.position_x_cloud, self.position_y_cloud))


if __name__ == '__main__':
    game = Game()
    game.play()
