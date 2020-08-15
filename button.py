import pygame.font

class Button:

    def __init__(self, ai_game, easy, medium, hard):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.width, self.height = 200, 50
        self.button_color = (0 ,255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect_easy = pygame.Rect(0, 0, self.width, self.height)
        self.rect_easy.centery = self.screen_rect.centery - 70
        self.rect_easy.centerx = self.screen_rect.centerx

        self.rect_medium = pygame.Rect(0, 0, self.width, self.height)
        self.rect_medium.centery = self.screen_rect.centery
        self.rect_medium.centerx = self.screen_rect.centerx

        self.rect_hard = pygame.Rect(0, 0, self.width, self.height)
        self.rect_hard.centery = self.screen_rect.centery + 70
        self.rect_hard.centerx = self.screen_rect.centerx

        self._prep_msg(easy, medium, hard)

    def _prep_msg(self, easy, medium, hard):
        self.easy_image = self.font.render(easy, True, self.text_color, self.button_color)
        self.medium_image = self.font.render(medium, True, self.text_color, self.button_color)
        self.hard_image = self.font.render(hard, True, self.text_color, self.button_color)

        self.easy_image_rect = self.easy_image.get_rect()
        self.easy_image_rect.center = self.rect_easy.center

        self.medium_image_rect = self.medium_image.get_rect()
        self.medium_image_rect.center = self.rect_medium.center

        self.hard_image_rect = self.hard_image.get_rect()
        self.hard_image_rect.center =self.rect_hard.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect_easy)
        self.screen.blit(self.easy_image, self.easy_image_rect)

        self.screen.fill(self.button_color, self.rect_medium)
        self.screen.blit(self.medium_image, self.medium_image_rect)

        self.screen.fill(self.button_color, self.rect_hard)
        self.screen.blit(self.hard_image, self.hard_image_rect)
