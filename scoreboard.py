import pygame.font
from pygame.sprite import Group

from player import Player


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, screen, stats):
        """Initialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.lives = Group()

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 45)

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, (255, 255, 255), (0, 0, 0))

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left
        self.score_rect.top = 5

    def prep_level(self):
        rounded_level = self.stats.level
        level_str = "{:,}".format(rounded_level)
        level_str = "Lvl: " + level_str
        self.level_image = self.font.render(level_str, True, (255, 255, 255), (0, 0, 0))

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right
        self.level_rect.top = 5

    def show_score(self):
        """Draw score ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships
        self.lives.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = int(round(self.stats.first_place, -1))
        high_score_str = "{:,}".format(high_score)
        high_score_str = "High Score: " + high_score_str
        self.high_score_image = self.font.render(high_score_str, True, (255, 255, 255), (0, 0, 0))

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        file = open("highscores.txt", "w")
        file.write(str(self.stats.first_place) + "\n")
        file.write(str(self.stats.second_place) + "\n")
        file.write(str(self.stats.third_place) + "\n")
        file.close()

    def prep_lives(self):
        """Show how many lives are left"""
        self.lives = Group()
        for life_number in range(self.stats.lives_left):
            player = Player(self.screen)
            player.rect.x = 10 + life_number * player.rect.width
            player.rect.y = 705
            self.lives.add(player)
