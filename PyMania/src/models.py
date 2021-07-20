import pygame
import time

from PyMania.src.helpers import load_animations
from PyMania.src.enums import PlayerAnimationStates
from PyMania.src.config import GRAVITY

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type: str, x: int, y: int, scale: int, speed: int, screen: pygame.Surface):
        super().__init__()
        self.animations = []
        self.index = 0
        self.action = 0
        self.screen = screen
        self.flip = False
        self.char_type = char_type
        self.speed = speed
        self._load_animations(scale)
        self.image = self.animations[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.udpate_time = pygame.time.get_ticks()
        self.attacking = False
        self.last_attacked = pygame.time.get_ticks()
        self.vel_y = 0
        self.vel_x = 0
        self.max_jumps = 2
        self.jumped_times = 0
        self.direction = 1
        
        

        # movement states

        self.moving_left = False
        self.moving_right = False
        self.is_jumping = False
        self.is_sliding = False
        self.in_air = False
        self.jump = False
        self.slide = False
        self.idle = True


    
    def _load_animations(self, scale: int):
        animation_types = ["idle", "run", "attack", "jump", "smrsl", "slide"]
        for a_type in animation_types:
            animation_directory = f"../animations/{self.char_type}/{a_type}"
            frames = load_animations(animation_directory, scale)
            self.animations.append(frames)

    def change_action(self, action: int):
        if self.action != action:
            self.action = action
            self.index = 0
            self.udpate_time = pygame.time.get_ticks()

    def draw(self):
        ANIMATION_COOLDOWN = 130
        animation_sequence = self.animations[self.action]

        frame = animation_sequence[self.index]
        frame = pygame.transform.flip(frame, self.flip, False)
        self.image = frame
        if pygame.time.get_ticks() - self.udpate_time > ANIMATION_COOLDOWN:
            self.index += 1
            self.udpate_time = pygame.time.get_ticks()

        if self.index >= len(animation_sequence):
            self.index = 0
            if self.attacking is True: 
                # if we are on the last attack animation frame, simply set attacking to false and wait
                # for the move method to handle the rest
                self.attacking = False
                self.change_action(PlayerAnimationStates.IDLE)
                self.idle = True

        self.screen.blit(self.image, self.rect)

    def move(self):
        dx = 0
        dy = 0
        self.idle = True if self.is_jumping is False else False
        

        
        
        if self.jump and self.in_air is False:
            self.vel_y = -11
            self.jump = False
            self.idle = False
            self.change_action(PlayerAnimationStates.SMRSL)
            self.is_jumping = True

        if self.slide and not self.jump and not self.is_sliding:
            self.vel_x = 5 * self.direction
            self.slide = False
            dx += self.vel_x
            self.is_sliding = True
            self.change_action(PlayerAnimationStates.SLIDE)

        if self.is_sliding:
            self.vel_x -= 0.1
            self.idle = False
            self.change_action(PlayerAnimationStates.SLIDE)
            if self.vel_x <= 0:
                self.vel_x = 0
                self.is_sliding = False

                

        if self.attacking:
            ATTACK_COOLDOWN = 75
            if pygame.time.get_ticks() - self.last_attacked > ATTACK_COOLDOWN:
                self.idle = False
                self.change_action(PlayerAnimationStates.ATTACK)
            else:
                self.attacking = False

        self.vel_y += GRAVITY
        if self.vel_y >= 10:
            self.vel_y = 10
        dy += self.vel_y
        
        if self.rect.bottom + dy >= 612:
            dy = 612 - self.rect.bottom
            self.in_air = False
            self.jumped_times = 0
            self.is_jumping = False


        if self.moving_left:
            dx = -self.speed
            self.idle = False
            self.flip = True
            if self.is_jumping:
                self.change_action(PlayerAnimationStates.SMRSL)
            elif self.is_sliding:
                self.change_action(PlayerAnimationStates.SLIDE)
            else:
                self.change_action(PlayerAnimationStates.RUN) if self.attacking is False else self.change_action(PlayerAnimationStates.ATTACK)

        elif self.moving_right:
            dx = self.speed
            self.idle = False
            self.flip = False
            if self.is_jumping:
                self.change_action(PlayerAnimationStates.SMRSL)
            elif self.is_sliding:
                self.change_action(PlayerAnimationStates.SLIDE)
            else:
                self.change_action(PlayerAnimationStates.RUN) if self.attacking is False else self.change_action(PlayerAnimationStates.ATTACK)



        if self.idle:
            """dx = 0
            dy = 0"""
            self.change_action(PlayerAnimationStates.IDLE)

        self.rect.x += dx
        self.rect.y += dy




