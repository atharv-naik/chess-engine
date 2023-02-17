import pygame


class Button():
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hover = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def is_clicked(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        #  check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                action = True
                self.clicked = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        return action
