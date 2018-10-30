import pygame
from pygame.sprite import Sprite
from pygame import mixer
import math


class Ghost(Sprite):

    def __init__(self,  screen, type):
        """Initialize the ship and set its starting position"""
        super(Ghost, self).__init__()
        self.screen = screen
        self.speed_factor = 1
        self.y_mod = 20
        self.vulnerable = False
        self.cycle = False
        self.in_spawn = True
        self.timer = 0
        self.type = type
        self.destinationx = 0
        self.destinationy = 0
        mixer.init()

        # Load the ship image and get its rect
        if self.type == 0:
            self.image = pygame.image.load('images/red.png')
            self.y_mod += 70
            x = 0
        elif self.type == 1:
            self.image = pygame.image.load('images/pink.png')
            x = -40
        elif self.type == 2:
            self.image = pygame.image.load('images/blue.png')
            x = 0
        elif self.type == 3:
            self.image = pygame.image.load('images/orange.png')
            x = 40
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx + x
        self.rect.centery = self.screen_rect.centery - self.y_mod

        # Store a decimal value for the ship's center
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ghost's position based on the movement flag"""
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center_x -= self.speed_factor
        elif self.moving_down and self.rect.centery < self.screen_rect.bottom:
            self.center_y += self.speed_factor
        elif self.moving_up:
            self.center_y -= self.speed_factor

        if self.vulnerable:
            self.timer -= 1
            if self.timer % 100 == 0:
                self.cycle = not self.cycle

            if not self.cycle:
                self.image = pygame.image.load('images/scared.png')
            else:
                self.image = pygame.image.load('images/scared2.png')

            if self.timer <= 0:
                self.timer = 0
                self.vulnerable = False
        else:
            if self.type == 0:
                self.image = pygame.image.load('images/red.png')
            elif self.type == 1:
                self.image = pygame.image.load('images/pink.png')
            elif self.type == 2:
                self.image = pygame.image.load('images/blue.png')
            elif self.type == 3:
                self.image = pygame.image.load('images/orange.png')

        # Update rect object from self.center
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def reset_ghost(self):
        # Load the ship image and get its rect
        if self.type == 0:
            self.image = pygame.image.load('images/red.png')
            self.y_mod += 70
            x = 0
        elif self.type == 1:
            self.image = pygame.image.load('images/pink.png')
            x = -40
        elif self.type == 2:
            self.image = pygame.image.load('images/blue.png')
            x = 0
        elif self.type == 3:
            self.image = pygame.image.load('images/orange.png')
            x = 40
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx + x
        self.rect.centery = self.screen_rect.centery - self.y_mod

        # Store a decimal value for the ship's center
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def set_vulnerable(self):
        self.vulnerable = True
        self.timer = 1000

    def move_left(self):
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def move_right(self):
        self.moving_left = False
        self.moving_right = True
        self.moving_up = False
        self.moving_down = False

    def move_up(self):
        self.moving_left = False
        self.moving_right = False
        self.moving_up = True
        self.moving_down = False

    def move_down(self):
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = True

    def decide_direction(self, x, y, bricks):
        wall_left = self.check_wall(bricks, "left")
        wall_right = self.check_wall(bricks, "right")
        wall_up = self.check_wall(bricks, "up")
        wall_down = self.check_wall(bricks, "down")

        if x > y:
            if self.destinationx < self.rect.centerx:
                if not wall_left:
                    self.move_left()
                else:
                    if self.destinationy > self.rect.centery:
                        if not wall_down:
                            self.move_down()
                    else:
                        if not wall_up:
                            self.move_up()
            else:
                if not wall_right:
                    self.move_right()
                else:
                    if self.destinationy > self.rect.centery:
                        if not wall_down:
                            self.move_down()
                    else:
                        if not wall_up:
                            self.move_up()
        else:
            if self.destinationy < self.rect.centery:
                if not wall_up:
                    self.move_up()
                else:
                    if self.destinationx < self.rect.centerx:
                        if not wall_left:
                            self.move_left()
                        else:
                            if not wall_right:
                                self.move_right()
            else:
                if not wall_down:
                    self.move_down()
                else:
                    if self.destinationx < self.rect.centerx:
                        if not wall_left:
                            self.move_left()
                        else:
                            if not wall_right:
                                self.move_right()

    def distance(self, x, y):
        tempx = self.distance_x(x)
        tempy = self.distance_y(y)

        return math.sqrt(tempx ** 2 + tempy ** 2)

    def distance_x(self, x):
        return abs(self.rect.centerx - x)

    def distance_y(self, y):
        return abs(self.rect.centery - y)

    def check_wall(self, bricks, dir):
        collision = False
        temp_rect = self.rect
        if dir == "right":
            self.rect.centerx += self.speed_factor
        elif dir == "left":
            self.rect.centerx -= self.speed_factor
        elif dir == "down":
            self.rect.centery += self.speed_factor
        elif dir == "up":
            self.rect.centery -= self.speed_factor

        for brick in bricks:
            if self.rect.colliderect(brick):
                collision = True

        if dir == "right":
            self.rect.centerx -= self.speed_factor
        elif dir == "left":
            self.rect.centerx += self.speed_factor
        elif dir == "down":
            self.rect.centery -= self.speed_factor
        elif dir == "up":
            self.rect.centery += self.speed_factor

        return collision

    def blinky(self, pacman, bricks):
        x = self.distance_x(pacman.rect.centerx)
        y = self.distance_y(pacman.rect.centery)

        # Exit Spawn
        if self.in_spawn:
            self.exit_spawn(bricks)
        else:
            # Set destination
            self.destinationx = pacman.rect.centerx
            self.destinationy = pacman.rect.centery

        # Decide direction to move to
        self.decide_direction(x, y, bricks)

    def exit_spawn(self, bricks):
        if self.rect.centerx == self.destinationx and self.rect.centery == self.destinationy:
            self.in_spawn = False
            return

        self.destinationx = self.screen_rect.centerx
        self.destinationy = self.screen_rect.centery - 90

    def choose_ai(self, pacman, bricks):
        if self.type == 0:
            self.blinky(pacman, bricks)
        elif self.type == 1:
            self.blinky(pacman, bricks)
        elif self.type == 2:
            self.blinky(pacman, bricks)
        elif self.type == 3:
            self.blinky(pacman, bricks)
