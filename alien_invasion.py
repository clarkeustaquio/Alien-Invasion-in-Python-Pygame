import sys
import pygame
from time import sleep
import json

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Alien Invasion")

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.stats = GameStats(self)
        self.scoreboard = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Easy", "Medium", "Hard")

        self._initialize_sounds()

    def run_game(self):
        while True:
            self._check_event()
            if self.stats.game_flag:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

            #print(len(self.bullets))

    def _start_game(self):
        if not self.stats.game_flag:
            self.stats.reset_stats()
            self.stats.game_flag = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)
            
    def _write_high_score(self):
        high_score_file = self.settings.high_score_file
        high_score = self.stats.high_score

        with open(high_score_file, 'w') as file_object:
            json.dump(high_score, file_object)

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._write_high_score()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_position):
        easy_button = self.play_button.rect_easy.collidepoint(mouse_position)
        medium_button = self.play_button.rect_medium.collidepoint(mouse_position)
        hard_button = self.play_button.rect_hard.collidepoint(mouse_position)

        if easy_button:
            self.settings.initialize_dynamic_settings()
            self._initialize_game()

        elif medium_button:
            self.settings.medium_game_settings()
            self._initialize_game()
        elif hard_button:
            self.settings.hard_game_settings()
            self._initialize_game()

    def _initialize_game(self):
        self._start_game()
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
    
    def _initialize_sounds(self):
        pygame.mixer.music.load(self.settings.game_music)
        pygame.mixer.music.play(-1)
        self.bullet_sound = pygame.mixer.Sound(self.settings.bullet_sound)
        self.collide_sound = pygame.mixer.Sound(self.settings.collide_sound)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            self._write_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_flag == True:
            self.bullet_sound.play()
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level +=1
            self.scoreboard.prep_level()
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.collide_sound.play()

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.scoreboard.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_flag = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_alien_bottom()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                        (3 * alien_height) - ship_height)

        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.y = alien_height + 2 * alien_height * row_number
            alien.rect.y = alien.y

            self.aliens.add(alien)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()

        if not self.stats.game_flag:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()