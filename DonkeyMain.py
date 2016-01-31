import os
import sys
import random
import time

import pygame
import basicSprite

from helpers import *
from pygame.locals import *
from playerSprite import *
import Fireball
from time import sleep



if not pygame.font:
    print 'Warning, Font Disabled'

if not pygame.mixer:
    print 'Warning, Sound Disabled'


BLOCK_SIZE = 22
FRAMES_PER_SECOND = 60
FIREBALL_CREATION = USEREVENT + 1
RELOAD_LEVEL = USEREVENT + 2
FLOAT_BLOCK = USEREVENT + 3
# Remember Base_X if not equal to Length_X


class GameMenu():
    """ Displays the Game menu"""

    def __init__(self, height, width):
        """ Initialise the Game menu using pygame.init()"""
        pygame.init()
        self.runGame = False
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((self.width,self.height), DOUBLEBUF)
        self.screen.fill((13,23,55))
        self.clock = pygame.time.Clock()
        deltat = self.clock.tick(FRAMES_PER_SECOND)


    def run(self):
        """ Display the Game Menu """
        mainloop = True
        self.message('### DonkeyKing ###','','','=> MENU <=', '','p = Play DonkeyKing','q = Quit Game')
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print 'END'
                    mainloop = False
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        print 'START'
                        mainloop = False
                        self.runGame = 1
                    elif event.key == K_q:
                        mainloop = False

            # Redraw the background
            pygame.display.flip()

    def message(self, *messages):
        """ Displays """
        textpos = 0
        counter=0
        centerX = self.width/2
        centerY = 30
        fontTemp = 30

        for msg in messages:
            if pygame.font:
                font = pygame.font.Font(None,fontTemp)
                text = font.render("%s" % (msg) ,1 ,(255,0,0))
                textpos = text.get_rect(centerx=centerX, centery = centerY + counter*25);
                self.screen.blit(text, textpos)
            counter += 1
            fontTemp = 20

        #self.background = pygame.image.load("data/images/background.png").convert();
        #self.screen.blit(self.background, [0, 0])
        pygame.display.flip()
        time.sleep(3)





class DonkeyMain:
    """ The most important class. It pertains the game logic and holds most of the work which the game does."""
    def __init__(self,height,width):
        """ Initialise pygame and some of the font and audio variables. """
        pygame.init()
        pygame.mixer.init()
        self.CURRENT_LEVEL = 001
        clock = pygame.time.Clock()
        deltat = clock.tick(FRAMES_PER_SECOND)
        self.height = height
        self.width = width
        self.FLOAT_INDEX = 0
        self.last_time = 0
        self.screen = pygame.display.set_mode((self.width,self.height), DOUBLEBUF)
        self.hearts = pygame.image.load('data/images/hearts.png').convert()
        self.sound_background = pygame.mixer.music.load('data/sound/background3.mp3')


    def MainLoop(self):
        """ Consists the game logic and keep the game running """
        pygame.key.set_repeat(300,30);
        self.LoadSprites(self.CURRENT_LEVEL)
        self.message('Level 1','---------------------------------------','Score: 0', 'Life: 3')
        pygame.time.set_timer(FIREBALL_CREATION, 5321);
        #pygame.time.set_timer(FLOAT_BLOCK, 403);

        while 1:
            self.player_sprites.clear(self.screen,self.background)
            self.donkey_sprites.clear(self.screen,self.background)
            for event in pygame.event.get():
                self.player.reset()
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_d)
                            or (event.key == K_a)
                            or (event.key == K_w)
                            or (event.key == K_s)):
                        self.player.MoveKeyDown(event.key, self.ladder_sprites, self.block_sprites)
                    elif (event.key == K_SPACE):
                        self.player._jump = 1
                    elif (event.key == K_q):
                        self.message('Bye Bye :P');
                        sleep(1)
                        sys.exit()
                elif event.type == FIREBALL_CREATION:
                    for donkey in self.donkey_sprites.sprites():
                        if pygame.mixer:
                            self.player.sound_fireball.play()
                        fireball = Fireball.Fireball(donkey.rect.center,0)
                        self.fireball_sprites.add(fireball)
                elif event.type == RELOAD_LEVEL:
                    #print 'Level Reloaded !!'

                    r = self.player.getCoins()
                    e = self.player._life
                    self.LoadSprites(str(int(self.CURRENT_LEVEL) + 1))
                    self.message('Level ' + str(self.CURRENT_LEVEL), '---------------------------------', 'New Coins: '+ str(int(r+50)), 'Extra Life: '+str(int(e)))
                    self.compute_lives(e);
                    self.player.collectCoin(r,1)
                    self.player.collectCoin(10)
                    self.player._life = e

            self.player.Move()

            if self.player._last_direction == 1:
                self.player.jumpR(self.block_sprites,self.ladder_sprites)
            else:
                self.player.jumpL(self.block_sprites, self.ladder_sprites)

            self.player.checkWall(self.block_sprites)
            self.player.checkCollision(self.block_sprites,self.fireball_sprites, self.queen_sprites, self.start_sprites, self.donkey_sprites)
            self.player.checkGravity(self.ladder_sprites, self.block_sprites)
            listCols = pygame.sprite.spritecollide(self.player, self.coin_sprites,True)
            self.player.collectCoin(len(listCols))
            self.compute_lives()

            # Consists the logic to have floating bricks.
            temp = pygame.time.get_ticks()
            if temp - self.last_time > 200:
                self.float_block(self.flyingblock_sprites);
                self.last_time = temp

            # Update the positios of fireball
            for fireball in self.fireball_sprites.sprites():
                fireball.update(self.block_sprites, self.start_sprites, self.flyingblock_sprites);

            # Do the Drawing ........
            self.screen.blit(self.background, (0,0));

            # FONT SUPPORT
            textpos = 0
            if pygame.font:
                font = pygame.font.Font(None,36)
                text = font.render("Level %s                   Coins %s         Extra Lives:" % (self.CURRENT_LEVEL, self.player.getCoins()) ,1 ,(25,0,0))
                textpos = text.get_rect(centerx=self.background.get_width()/2, centery=20)
                self.screen.blit(text, textpos)

            # Updates all the sprites on the screen
            self.block_sprites.draw(self.screen)
            self.flyingblock_sprites.draw(self.screen)
            self.coin_sprites.draw(self.screen)
            self.donkey_sprites.draw(self.screen)
            self.ladder_sprites.draw(self.screen)
            self.fireball_sprites.draw(self.screen)
            self.start_sprites.draw(self.screen)
            self.player_sprites.draw(self.screen)
            self.queen_sprites.draw(self.screen)
            self.blank_sprites.draw(self.screen)
            self.life_sprites.draw(self.screen)

            # Actual rendering on the screen
            pygame.display.flip()



    def LoadSprites(self, LEVEL):
        """ Creates all the sprites and loads new lovel whenever required."""
        x_offset = BLOCK_SIZE/2
        y_offset = BLOCK_SIZE/2

        LEVEL_NAME = 'level' + str(LEVEL)
        try:
            levelMOD = __import__(LEVEL_NAME)
            self.CURRENT_LEVEL = int(LEVEL)
            #print 'LOADING: Level %s' %(self.CURRENT_LEVEL)
        except:
            #print 'Next Level not found, End of Game: YOU WON !!'
            #import level1 as levelMOD
            #self.CURRENT_LEVEL = 1
            self.player.sound_win.play()
            self.background = pygame.image.load("data/images/background.png").convert();
            self.screen.blit(self.background, [0, 0])
            pygame.display.flip()
            self.message('Congratulations!!', 'You Have Won this Game & have becom the next SaVioUr.');
            time.sleep(3)
            sys.exit()


        # Imports the level from HDD
        level1 = levelMOD.level()
        layout = level1.getLayout()
        img_list = level1.getSprites()

        # Creates all the group that would hold all the sprites in future
        self.coin_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.donkey_sprites = pygame.sprite.Group()
        self.ladder_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()
        self.queen_sprites = pygame.sprite.Group()
        self.start_sprites = pygame.sprite.Group()
        self.blank_sprites = pygame.sprite.Group()
        self.flyingblock_sprites = pygame.sprite.Group()
        self.life_sprites = pygame.sprite.Group()

        # Check for the proper sprite and then group them
        for y in xrange(len(layout)):
            for x in xrange(len(layout[y])):
                centerPoint = [ (x*BLOCK_SIZE) + x_offset, (y*BLOCK_SIZE) + y_offset]
                if layout[y][x] == level1.BLOCK:
                    block = basicSprite.Sprite(centerPoint, img_list[level1.BLOCK])
                    self.block_sprites.add(block)
                elif layout[y][x] == level1.PLAYER:
                    self.player = Player(centerPoint, img_list[level1.PLAYER])
                    self.player.PLAYER_SPAWN_X = x
                    self.player.PLAYER_SPAWN_Y = y
                elif layout[y][x] == level1.DONKEY:
                    donkey = basicSprite.Sprite(centerPoint, img_list[level1.DONKEY])
                    self.donkey_sprites.add(donkey)
                elif layout[y][x] == level1.LADDER:
                    ladder = basicSprite.Sprite(centerPoint, img_list[level1.LADDER])
                    self.ladder_sprites.add(ladder)
                elif layout[y][x] == level1.LADDER2:
                    ladder = basicSprite.Sprite(centerPoint, img_list[level1.LADDER2])
                    self.ladder_sprites.add(ladder)
                elif layout[y][x] == level1.COIN:
                    coin = basicSprite.Sprite(centerPoint, img_list[level1.COIN])
                    self.coin_sprites.add(coin)
                elif layout[y][x] == level1.START:
                    start = basicSprite.Sprite(centerPoint, img_list[level1.START])
                    self.start_sprites.add(start)
                elif layout[y][x] == level1.QUEEN:
                    queen = basicSprite.Sprite(centerPoint, img_list[level1.QUEEN])
                    self.queen_sprites.add(queen)
                elif layout[y][x] == level1.FLYING_BLOCK:
                    fb = basicSprite.Sprite(centerPoint, img_list[level1.BLOCK])
                    self.block_sprites.add(fb)
                    self.flyingblock_sprites.add(fb)
                else:
                    blank = basicSprite.Sprite(centerPoint, img_list[level1.BLANK])
                    self.blank_sprites.add(blank)

        for x in range(self.player._life):
            BASE = 45*21;
            OFFSET = 40;
            self.life_sprites.add(basicSprite.Sprite((BASE + OFFSET*x,22), self.hearts));

        # Rest all the other stuff like = player display, background music, background_rendering etc.
        self.player_sprites = pygame.sprite.RenderPlain((self.player))
        self.background = pygame.image.load("data/images/background.png").convert();
        self.screen.blit(self.background, [0, 0])
        if pygame.mixer:
            pygame.mixer.music.play()
        pygame.display.flip()


    def message(self, *messages):
        """ Polymorphism: Prints all the strings that are given so that we may have a dynamic printing function. It prints the first string in a very big font, rest all are printed in a normal font."""
        textpos = 0
        counter=0
        centerX = self.background.get_width()/2
        centerY = self.background.get_height()/2
        fontTemp = 40

        for msg in messages:
            if pygame.font:
                font = pygame.font.Font(None,fontTemp)
                text = font.render("%s" % (msg) ,1 ,(255,0,0))
                textpos = text.get_rect(centerx=centerX, centery = centerY + counter*25);
                self.screen.blit(text, textpos)
            counter += 1
            fontTemp = 27

        #self.background = pygame.image.load("data/images/background.png").convert();
        #self.screen.blit(self.background, [0, 0])
        pygame.display.flip()
        time.sleep(3)



    def compute_lives(self, lives=None):
        if lives!=None:
            self.player._DEATH = 1;
            self.player._life = lives

        if self.player._DEATH:
            self.life_sprites.empty()
            for x in range(self.player._life):
                BASE = 45*21;
                OFFSET = 40;
                self.life_sprites.add(basicSprite.Sprite((BASE + OFFSET*x,22), self.hearts));
            self.player._DEATH = 0


    def float_block(self, block_group):
        """ Updates th eindexes of all the bricks that float in the air"""
        if self.FLOAT_INDEX == -1:
            return;

        D = [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2]
        for sp in block_group.sprites():
            sp.rect.move_ip(0,D[self.FLOAT_INDEX])
        while pygame.sprite.groupcollide(self.player_sprites, self.flyingblock_sprites,False,False,collided=None):
            self.player.rect.move_ip(0,-1);
        self.FLOAT_INDEX += 1
        if self.FLOAT_INDEX >= len(D):
            self.FLOAT_INDEX = 0

if __name__=="__main__":
    """ Starts the Donkey King Game """
    M = GameMenu(300,200)
    M.run()
    if M.runGame:
        MainWindow = DonkeyMain(BASE_Y,BASE_X)
        MainWindow.MainLoop()


