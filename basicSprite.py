import pygame
from pygame.locals import *
import random


class Sprite(pygame.sprite.Sprite):
    """ It is the most basic sprite that contains all the variable that are required by the pygame to function."""

    def __init__(self, centerPoint, image):
        """ Instantize the Sprite"""
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = centerPoint


class Coin(pygame.sprite.Sprite):
    """ Class that denotes all the coin counting """

    def __init__(self, top_left, image=None):
        """ Instantize the coin data."""
        pygame.sprite.Sprite.__init__(self)
        if image == None:
            self.image, self.rect = load_image('coin.png',-1)
        else:
            self.image = image
            self.rect = image.get_rect()

        self.rect.topleft = top_left
