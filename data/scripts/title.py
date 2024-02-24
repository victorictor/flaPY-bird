import pygame as pg
from random import randint
class TITLE:
    def __init__(self):
        img = pg.transform.scale_by(pg.image.load('data/img/flapy.png').convert_alpha(), 4)
        rects = [
            (0, 0, 37, 70),
            (37, 0, 36, 59),
            (73, 0, 51, 68), 
            (124, 0, 41, 64),
            (165, 0, 46, 70)]

        rects_x4 = [(x*4, y*4, w*4, h*4) for (x,y,w,h) in rects]
        self.letras = [pg.Surface.subsurface(img, rect) for rect in rects_x4]
        
        self.pos = [8, 256]
        self.vel = 0
        self.grav = 20.5
        self.framecount = 0

    def pulo(self, dt):
        self.framecount = (self.framecount + 1) % 15
        if self.framecount == 0:
            self.pos[1] -= 50
            self.pulando = True

        if self.pos[1] < 256:
            self.pos[1] -= 60
            if self.pos[1] >= 256:
                self.pos = 256
        
    def draw(self, tela):
        '''for i, letra in enumerate(reversed(self.letras)):
            self.pos = [(len(self.letras) - 1 - i) * 150 + 8, (len(self.letras) - 1 - i) * -60 + 256]
            tela.blit(letra, self.pos)'''
        
        tela.blit(self.letras[0], (self.pos[0],self.pos[1]))

    def update(self, tela, dt):
        
        self.pulo(dt)
        self.draw(tela)