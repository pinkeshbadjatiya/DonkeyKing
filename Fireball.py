#! /usr/bin/env python

import basicSprite
from helpers import *
import random
import pygame
from pygame.locals import *

class Fireball(pygame.sprite.Sprite):
    """ Defines fireball for all levels just for optimisation """

    def __init__(self, coor, direc):
        pygame.sprite.Sprite.__init__(self,)
        fireball, rect = load_image('fireball.png',-1)
        self.image = fireball
        self.rect = rect
        self.rect.center = coor
        self.Hdir = direc
        #print coor


    def update(self, block_group, start_group, flyingblock_group):
        """ Updates the position of the fireball"""
        # 0 = Go bottom
        # 1 = Go right
        # -1 = Go left
        while pygame.sprite.spritecollide(self,flyingblock_group, False):
            self.rect.move_ip(0,-1);

        if self.Hdir == 0:
            # For ball going downwards
            self.rect.move_ip(0,1)
            if pygame.sprite.spritecollide(self, block_group, False):
                self.Hdir = random.randint(0,1);
                self.rect.move_ip(0,-1)
                #print 'Fireball Cannot penetrate surface'
                if self.Hdir == 0:
                    self.Hdir = -1
                #print 'New Direction = %s' % self.Hdir
        elif self.Hdir == 1:
            # For ball going right
            self.rect.move_ip(0,1)
            if pygame.sprite.spritecollide(self, block_group, False):
                self.rect.move_ip(1,-1)
                if pygame.sprite.spritecollide(self, block_group, False):
                    self.rect.move_ip(-1,0)
                    #print 'Encountered a Wall, reversing direction'
                    self.Hdir = -1
            else:
                #print 'Ball Can Move Down'
                #print 'New Direction = 0'
                self.Hdir = 0
        elif self.Hdir == -1:
            # For ball going towards left
            self.rect.move_ip(0,1)
            if pygame.sprite.spritecollide(self, block_group, False):
                self.rect.move_ip(-1,-1)
                if pygame.sprite.spritecollide(self, block_group, False):
                    self.rect.move_ip(1,0)
                    #print 'Encountered a Wall, reversing direction'
                    self.Hdir = 1
            else:
                #print 'Ball Can Move Down'
                #print 'New Direction = 0'
                self.Hdir = 0
        else:
            while pygame.sprite.spritecollide(self, flyingblock_group, False):
                self.rect.move_ip(0,-1);
            print '********* DIRECTION UnKnown*********'



