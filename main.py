import pygame
import os
import sys
import math
import random
import time

pygame.font.init()

HEIGHT = 720

pygame.display.set_caption("Game")
plik = pygame.image.load('assets/images/night.png')
main_font = pygame.font.SysFont("comicsans", 50)
wynik = 0
zycia = 3

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Player(object):
    COOLDOWN = 30
    laser_img = pygame.image.load('assets/images/laser.png')

    def __init__(self):
        self.image = pygame.image.load(os.path.join('assets/images', 'player.png'))
        self.center = [100, 200]
        self.lasers = []
        self.cool_down_counter = 0

    def move(self, x, y):
        self.center[0] += x
        self.center[1] += y

        if self.center[0] < 0:
            self.center[0] = 0
        if self.center[1] < 0:
            self.center[1] = 0
        if self.center[0] > 1280-68:
            self.center[0] = 1280-68
        if self.center[1] > 720-48:
            self.center[1] = 720-48

    def draw(self, surf):
        surf.blit(self.image, self.center)
        for laser in self.lasers:
            laser.draw(surf)

    def move_lasers(self, vel, ene):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                koli = collide2(laser, ene)
                if koli:
                    ene.center[0] = 96
                    ene.center[1] = 69
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.center[0], self.center[1], self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    

class Money(object):
    def __init__(self):
        self.image = pygame.image.load(os.path.join('assets/images', 'cash.png'))
        self.center = [400, 400]

    def move(self, x, y):
        self.center[0] += x
        self.center[1] += y

        if self.center[0] < 0:
            self.center[0] = 0
        if self.center[1] < 0:
            self.center[1] = 0
        if self.center[0] > 1280-68:
            self.center[0] = 1280-68
        if self.center[1] > 720-48:
            self.center[1] = 720-48

    def draw(self, surf):
        surf.blit(self.image, self.center)

class Atak(object):
    def __init__(self):
        self.image = pygame.image.load(os.path.join('assets/images', 'godzilla.png'))
        self.center = [800, 600]

    def move(self, x, y):
        self.center[0] += x
        self.center[1] += y

        if self.center[0] < 0:
            self.center[0] = 0
        if self.center[1] < 0:
            self.center[1] = 0
        if self.center[0] > 1280-68:
            self.center[0] = 1280-68
        if self.center[1] > 720-48:
            self.center[1] = 720-48

    def draw(self, surf):
        surf.blit(self.image, self.center)

def collide(obj1, obj2):
    offsetX = abs(obj1.center[0] - obj2.center[0])
    offsetY = abs(obj1.center[1] - obj2.center[1])
    return (offsetX < 40 and offsetY < 40)

def collide2(obj1, obj2):
    offsetX = abs(obj1.x - obj2.center[0])
    offsetY = abs(obj1.y - obj2.center[1])
    return (offsetX < 40 and offsetY < 40)


class Game(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.diax = Money()
        self.ata = Atak()

    def run(self):
        global zycia
        global wynik

        running = 1
        while running:
            self.clock.tick(60)
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = 0

            keys = pygame.key.get_pressed()
            move_x = keys[pygame.K_d] - keys[pygame.K_a]
            move_y = keys[pygame.K_s] - keys[pygame.K_w]
            self.player.move(move_x * 5, move_y * 5)
            self.screen.blit(plik, (0, 0))

            if keys[pygame.K_SPACE]:
                self.player.shoot()

            distX = self.player.center[0] - self.ata.center[0]
            distY = self.player.center[1] - self.ata.center[1]

            self.ata.move(distX * 0.04, distY * 0.04)
            
            isColide = collide(self.player, self.diax)
            if isColide:
                wynik = wynik + 1
                self.diax.center[0] = random.randint(40, 1200)
                self.diax.center[1] = random.randint(40, 650)
                if wynik == 50:
                    wn = main_font.render(f"You Win", 1, (255, 50, 255))
                    self.screen.blit(wn, (700 - wn.get_width() - 10, 10))
                    running = 0
            
            tisColide = collide(self.player, self.ata)
            if tisColide:                
                zycia = zycia - 1
                self.ata.center[0] = 0
                self.ata.center[1] = 40
                if zycia == 0:
                    geme = main_font.render(f"You Lose", 1, (255, 50, 255))
                    self.screen.blit(geme, (695 - geme.get_width() - 10, 10))
                    running = 0              

            
                         
                

            self.player.move_lasers(-7.5, self.ata)

            self.ata.draw(self.screen)
            self.diax.draw(self.screen)
            self.player.draw(self.screen)

            level_label = main_font.render(f"Score: {wynik}", 1, (255, 255, 255))               
            self.screen.blit(level_label, (1280 - level_label.get_width() - 10, 10))
            level_labele = main_font.render(f"Lives: {zycia}", 1, (255, 255, 255))
            self.screen.blit(level_labele, (142 - level_labele.get_width() - 10, 10))

            pygame.display.update()

            if running == 0:
                time.sleep(2)

g = Game()
g.run()