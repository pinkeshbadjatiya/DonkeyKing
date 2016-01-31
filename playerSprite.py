import pygame
import basicSprite
from pygame.locals import *
from helpers import *

BASE_Y = 630
BASE_X = 1300

PLAYER_SPAWN_X = 99
PLAYER_SPAWN_Y = 540
RELOAD_LEVEL = USEREVENT + 2

class Player(basicSprite.Sprite):

    def __init__(self, centerPoint, image):
        basicSprite.Sprite.__init__(self, centerPoint, image)
        self.sound_coin = pygame.mixer.Sound('data/sound/coin.wav')
        self.sound_coin.set_volume(0.4)
        self.sound_fireball = pygame.mixer.Sound('data/sound/fireball.wav')
        self.sound_buzzer = pygame.mixer.Sound('data/sound/buzzer.wav')
        self.sound_win = pygame.mixer.Sound('data/sound/win.wav')
        self.sound_fireball.set_volume(0.4)

        self.x_dist = 1
        self.y_dist = 1

        self.__coins = 0
        self.__xMove = 0
        self.__yMove = 0

        self._life = 3
        self._jump_index = 1
        self._jump = 0
        self._last_direction = 1
        self._DEATH = 0

    def getPosition(self):
        #print self.rect.center
        return self.rect.center;

    def reset(self):
        self.__xMove = 0
        self.__yMove = 0

    def getCoins(self):
        #print self.__coins
        return self.__coins;

    def checkWall(self,block_group):
        if pygame.sprite.spritecollide(self,block_group, False):
            self.rect.move_ip(-self.__xMove, -self.__yMove)


    def checkCollision(self, block_group, fireball_group, queen_group, start_group, monster_group):
        if pygame.sprite.spritecollide(self,block_group, False):
            self.rect.move_ip(-self.__xMove, -self.__yMove)
        elif pygame.sprite.spritecollide(self,fireball_group, False) or pygame.sprite.spritecollide(self,monster_group, False):
            # RESTART GAME,
            self.sound_buzzer.play()
            self.rect.move_ip(PLAYER_SPAWN_X-self.rect[0],PLAYER_SPAWN_Y-self.rect[1])
            fireball_group.empty()
            self.__coins -= 25
            self._life -= 1
            self._DEATH = 1

            if self._life <0:
                sys.exit()
            #print 'COLLISION: Fireball'
        elif pygame.sprite.spritecollide(self,queen_group,False):
            pygame.event.post(pygame.event.Event(RELOAD_LEVEL,{}))

        pygame.sprite.groupcollide(start_group, fireball_group, False ,True, collided=None);
        #    print 'Fireball Deleted'




    def collectCoin(self,coins,overwrite=0):
        if overwrite:
            self.__coins = coins;
        else:
            self.__coins = self.__coins + coins*5
            if coins and pygame.mixer:
                self.sound_coin.play()

    def checkGravity(self, ladder_group, block_group):
        """ Keeps the player on the surface providing the gravity effect"""
        if pygame.sprite.spritecollide(self,ladder_group, False):
            pass
            #print 'Ladder Collide, ACCEPTED'
        else:
            # Check if there if floor below
            self.rect.move_ip(0, 1)
            if pygame.sprite.spritecollide(self,block_group, False):
                # Floor below, reverse movement
                self.rect.move_ip(0, -1)
            elif pygame.sprite.spritecollide(self,ladder_group,False):
                # Do nothing
                self.rect.move_ip(0, -1)


    def MoveKeyDown(self, key, ladder_group, block_group):
        """This function sets the xMove or yMove variables that will
        then move the snake when update() function is called.  The
        xMove and yMove values will be returned to normal when this
        keys MoveKeyUp function is called."""

        if (key == K_d):
            self.__xMove += self.x_dist
            self._last_direction = 1
        elif (key == K_a):
            self.__xMove += -self.x_dist
            self._last_direction = -1
        elif (key == K_w):
            self.__yMove += -self.y_dist
        elif (key == K_s):
            self.__yMove += self.y_dist

    def MoveKeyUp(self, key):
        """This function resets the xMove or yMove variables that will
        then move the snake when update() function is called.  The
        xMove and yMove values will be returned to normal when this
        keys MoveKeyUp function is called."""

        if (key == K_d):
            self.__xMove += -self.x_dist
        elif (key == K_a):
            self.__xMove += self.x_dist
        elif (key == K_w):
            self.__yMove += self.y_dist
        elif (key == K_s):
            self.__yMove += -self.y_dist

    def Move(self):
        self.rect.move_ip(self.__xMove,self.__yMove)

    def jumpR(self, block_group, ladder_group):
        """ Check and doed the jumping of the player"""
        self.rect.move_ip(0,1)
        if self._jump_index == 1 and (not pygame.sprite.spritecollide(self,block_group,False) and (not pygame.sprite.spritecollide(self,ladder_group,False))):
            self.rect.move_ip(0,-1);
            self._jump = 0
            return;
        else:
            self.rect.move_ip(0,-1)

        if self._jump == 1:
            X = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,0]
            Y = [0,-4,-4,-4,-3,-3,-3,-3,-3,-2,-2,-2,-2,-1,-2,-2,-1,-2,-2,-2,-1,-2,-2,-2,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,2,2,2,2,2,2,0,2,3,3,3,3,3,3,3,3,2]
            M = self._jump_index
            self._jump_index += 1
            if M < len(X):
                self.rect.move_ip(X[M],Y[M])
                if pygame.sprite.spritecollide(self,block_group, False):
                    self.rect.move_ip(-X[M], -Y[M])
                    self._jump = 0
                    self._jump_index = 1
            else:
                self._jump = 0
                self._jump_index = 1

    def jumpL(self, block_group, ladder_group):
        """ Check and do the jumping of the player"""
        self.rect.move_ip(0,1)
        if self._jump_index==1 and (not pygame.sprite.spritecollide(self,block_group,False) and (not pygame.sprite.spritecollide(self,ladder_group,False))):
            self.rect.move_ip(0,-1);
            self._jump = 0
            return;
        else:
            self.rect.move_ip(0,-1)

        if self._jump == 1:
            X = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,0]
            Y = [0,-4,-4,-4,-3,-3,-3,-3,-3,-2,-2,-2,-2,-1,-2,-2,-2,-1,-2,-2,-1,-2,-2,-2,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,2,2,2,2,2,2,0,2,3,3,3,3,3,3,3,3,2]
            M = self._jump_index
            self._jump_index += 1
            if M < len(X):
                self.rect.move_ip(-X[M],Y[M])
                if pygame.sprite.spritecollide(self,block_group, False):
                    self.rect.move_ip(X[M], -Y[M])
                    self._jump = 0
                    self._jump_index = 1
            else:
                self._jump = 0
                self._jump_index = 1

