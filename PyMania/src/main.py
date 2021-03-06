import pygame
import threading
import os

from PyMania.src.config import *
from PyMania.src.models import Player


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("PyMania!")

game_loop_event = threading.Event()
game_clock = pygame.time.Clock()
background_image = pygame.image.load("../assets/images/background.jpg")
player = Player("explorer", 200, 200, 3, 4, screen)


while not game_loop_event.is_set():
    game_clock.tick(FPS)

    screen.fill(BACKGROUND_COLOUR)
    screen.blit(background_image, (0, 175))
    pygame.draw.line(screen, RED, (0, 612), (SCREEN_WIDTH, 612))
    player.draw()
    player.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop_event.set()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving_left = True
            elif event.key == pygame.K_d:
                player.moving_right = True
            
            if event.key == pygame.K_c:
                player.slide = True

            if event.key == pygame.K_SPACE:
                player.jump = True if player.in_air is False else False
            
            if event.key == pygame.K_ESCAPE:
                game_loop_event.set()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False
            elif event.key == pygame.K_d:
                player.moving_right = False

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
            player.attacking = True
        """elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pressed()[0] == 0:
            player.attacking = False"""

    pygame.display.update()



pygame.quit()