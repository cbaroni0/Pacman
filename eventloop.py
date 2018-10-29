import pygame
import sys
import array
from pygame.sprite import Sprite
from player import Player
from pygame import mixer


class EventLoop:
    def __init__(self, finished):
        self.finished = finished

    def __str__(self):
        return 'eventloop, finished=' + str(self.finished) + ')'

    #@staticmethod
    def check_events(self, screen, player, maze, stats, button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #sys.exit()
                self.finished = True
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event, screen, player, maze)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event, screen, player)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(stats, button, mouse_x, mouse_y)

    def check_play_button(self, stats, button, mouse_x, mouse_y):
        """Start a new game when the player clicks Play"""
        button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            stats.game_active = True

    def check_keydown_events(self, event, screen, player, maze):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            player.moving_right = True
            player.moving_up = False
            player.moving_left = False
            player.moving_down = False
        elif event.key == pygame.K_LEFT:
            player.moving_right = False
            player.moving_up = False
            player.moving_left = True
            player.moving_down = False
        elif event.key == pygame.K_UP:
            player.moving_right = False
            player.moving_up = True
            player.moving_left = False
            player.moving_down = False
        elif event.key == pygame.K_DOWN:
            player.moving_right = False
            player.moving_up = False
            player.moving_left = False
            player.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

        if player.moving_right or player.moving_left or player.moving_up or player.moving_down:
            if not mixer.music.get_busy():
                mixer.music.load("sounds/pacman_chomp.wav")
                mixer.music.play(10)

    def check_wall_collision(self, player, maze):
        collision = False
        for brick in maze.bricks:
            #if pygame.sprite.collide_rect(player, brick):
            if player.rect.colliderect(brick):
                collision = True

        if collision:
            if player.moving_right:
                player.moving_right = False
                player.center_x -= player.speed_factor * 2
            elif player.moving_left:
                player.moving_left = False
                player.center_x += player.speed_factor * 2
            elif player.moving_up:
                player.moving_up = False
                player.center_y += player.speed_factor * 2
            elif player.moving_down:
                player.moving_down = False
                player.center_y -= player.speed_factor * 2

    def check_pill_collision(self, player, maze, stats):
        counter = 0
        for pill in maze.powerpills:
            # if pygame.sprite.collide_rect(player, brick):
            if player.rect.colliderect(pill):
                del maze.powerpills[counter]
                stats.score += 10
                #checks if all powerpills gone
                if not maze.powerpills:
                    stats.level += 1
                    player.reset_player()
                    maze.build()
            counter += 1

    def check_killpill_collision(self, player, maze, stats):
        counter = 0
        for pill in maze.killpills:
            if player.rect.colliderect(pill):
                del maze.killpills[counter]
                for ghost in maze.ghosts:
                    ghost.set_vulnerable()
                stats.score += 20
                player.invincible = True
            counter += 1

    def check_keyup_events(self, event, screen, player):
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            player.moving_right = False
        elif event.key == pygame.K_LEFT:
            player.moving_left = False
        elif event.key == pygame.K_UP:
            player.moving_up = False
        elif event.key == pygame.K_DOWN:
            player.moving_down = False

        if not player.moving_right and not player.moving_left and not player.moving_up and not player.moving_down:
            mixer.music.stop()
