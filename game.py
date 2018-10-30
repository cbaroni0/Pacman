import pygame
from maze import Maze
from eventloop import EventLoop
from player import Player
from scoreboard import Scoreboard
from game_stats import GameStats
from button import Button


class Game:
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 740))
        pygame.display.set_caption("Pacman Portal")
        self.button = Button(self.screen, "Start")

        self.player = Player(self.screen)

        self.maze = Maze(self.screen, mazefile='pacman_portal_maze_dots.txt',
                         brickfile='square', shieldfile='shield', portalfile='portal',
                         powerpill='powerpill', killpill='killpill')

        self.stats = GameStats()
        self.score_board = Scoreboard(self.screen, self.stats)

    def __str__(self): return 'Game(Pacman Portal), maze=' + str(self.maze) + ')'

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.first_place:
            self.stats.third_place = self.stats.second_place
            self.stats.second_place = self.stats.first_place
            self.stats.first_place = self.stats.score
            self.score_board.prep_high_score()
        elif self.stats.score > self.stats.second_place:
            self.stats.third_place = self.stats.second_place
            self.stats.second_place = self.stats.score
            self.score_board.prep_high_score()
        elif self.stats.score > self.stats.third_place:
            self.stats.third_place = self.stats.score
            self.score_board.prep_high_score()

    def play(self):
        eloop = EventLoop(finished=False)

        while not eloop.finished:
            eloop.check_events(self.screen, self.player, self.maze, self.stats, self.button)
            if self.stats.game_active:
                eloop.check_wall_collision(self.player, self.maze)
                eloop.check_pill_collision(self.player, self.maze, self.stats)
                eloop.check_killpill_collision(self.player, self.maze, self.stats)
                self.player.update()
            self.update_screen()
        self.check_high_score()
        self.score_board = Scoreboard(self.screen, self.stats)
        self.score_board.prep_high_score()

    def update_screen(self):
        self.screen.fill(Game.BLACK)
        self.player.blitme()
        if self.stats.game_active:
            self.maze.update_pacman(self.player)
            self.maze.blitme()
        self.score_board.prep_score()
        self.score_board.prep_level()
        self.score_board.show_score()

        ##############################################################
        # MAIN MENU
        ##############################################################
        if not self.stats.game_active:
            self.screen.fill((0, 0, 0))
            pygame.font.init()
            myfont = pygame.font.SysFont('Comic Sans MS', 20)
            self.button.draw_button()
            img = pygame.image.load('images/red.png')
            self.screen.blit(img, (200, 150))
            textsurface = myfont.render('= 10 points', True, (0, 255, 0))
            self.screen.blit(textsurface, (300, 155))
            img = pygame.image.load('images/pink.png')
            self.screen.blit(img, (200, 200))
            textsurface = myfont.render('= 20 points', True, (0, 255, 0))
            self.screen.blit(textsurface, (300, 205))
            img = pygame.image.load('images/blue.png')
            self.screen.blit(img, (200, 250))
            textsurface = myfont.render('= 40 points', True, (0, 255, 0))
            self.screen.blit(textsurface, (300, 255))
            img = pygame.image.load('images/orange.png')
            self.screen.blit(img, (200, 300))
            textsurface = myfont.render('= ????', True, (0, 255, 0))
            self.screen.blit(textsurface, (300, 305))
            myfont = pygame.font.SysFont('Comic Sans MS', 30)
            textsurface = myfont.render('Pacman', True, (0, 255, 0))
            self.screen.blit(textsurface, (300, 100))
            textsurface = myfont.render('High Scores', True, (0, 255, 0))
            self.screen.blit(textsurface, (300, 500))
            textsurface = myfont.render(str(self.stats.first_place), True, (255, 255, 255))
            self.screen.blit(textsurface, (300, 550))
            textsurface = myfont.render(str(self.stats.second_place), True, (255, 255, 255))
            self.screen.blit(textsurface, (300, 600))
            textsurface = myfont.render(str(self.stats.third_place), True, (255, 255, 255))
            self.screen.blit(textsurface, (300, 650))
        pygame.display.flip()


game = Game()
game.play()
