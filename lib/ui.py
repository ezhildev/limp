from config import *

class Text(pygame.sprite.Sprite):
    '''Text class used to make a Text object'''
    def __init__(self, text, font = FONT_M, color = 'white', position = (0, 0)) -> None:
        super().__init__() 
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = position
