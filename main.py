import pygame as pg
from sys import exit  

from data.scripts.bird import BIRD
from data.scripts.canos import CANO
from data.scripts.bg import BG
from data.scripts.title import TITLE


pg.init()

tela = pg.display.set_mode((800, 600)) 
clock = pg.time.Clock()
G = 9.807

bg = BG()
bird = BIRD()  
cano = CANO()
title = TITLE()   

class JOGO:
    def __init__(self):
        self.cena_atual = 'menu'

        font = pg.font.Font('data/img/Daydream.ttf', 30)
        self.text = font.render('SPACE to START', True, 'white')
        self.logo = pg.transform.scale_by(pg.image.load('data/img/logo.png').convert_alpha(), 4)

    def menu(self):
        dt = clock.tick(144)/1000.0
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                exit()
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    self.cena_atual = 'game'

        tela.fill((63, 93, 251))
        bg.update(tela, dt)
        #title.update(tela, dt)
        tela.blit(self.logo,(0,0))
        tela.blit(self.text, (300 - 90, 600 - self.text.get_height()))
        pg.display.flip()
        clock.tick()

    def game(self): 
        tela.fill((63, 93, 251))
        
        dt = clock.tick(144)/1000.0
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                quit()

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    bird.pulo(dt)

        bg.update(tela, dt)   
        cano.update(tela, dt)
        bird.update(tela, dt, cano.rectlist, self.cena_atual)
        pg.display.flip()
        clock.tick()

    def trocar_cena(self):
        if self.cena_atual == 'menu':
            self.menu()

        if self.cena_atual == 'game':
            clock.tick()
            self.game()

cenas = JOGO()
while True:
    cenas.trocar_cena()