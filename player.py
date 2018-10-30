import pygame
from pygame.sprite import Sprite
from pygame import mixer


class Player(Sprite):

    def __init__(self,  screen):
        """Initialize the ship and set its starting position"""
        super(Player, self).__init__()
        self.screen = screen
        self.speed_factor = 1
        self.y_mod = 200
        self.invincible = False
        mixer.init()

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/pacman.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - self.y_mod

        # Store a decimal value for the ship's center
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center_x -= self.speed_factor
        elif self.moving_down and self.rect.centery < self.screen_rect.bottom:
            self.center_y += self.speed_factor
        elif self.moving_up:
            self.center_y -= self.speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def reset_player(self):
        """Reset the player on the screen"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - self.y_mod

        # Store a decimal value for the ship's center
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)
