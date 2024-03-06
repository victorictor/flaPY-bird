import pygame as pg
from random import randint, uniform
class TITLE:
    def __init__(self):
        img = pg.transform.scale_by(pg.image.load('data/img/flapy.png').convert_alpha(), 4)
        cut_pos = [
            (0, 0, 37, 70),
            (37, 0, 36, 59),
            (73, 0, 51, 68), 
            (124, 0, 41, 64),
            (165, 0, 46, 70)]

        cot_pos_x4 = [(x*4, y*4, w*4, h*4) for (x,y,w,h) in cut_pos]
        self.letras = [pg.Surface.subsurface(img, rect) for rect in cot_pos_x4]
        self.letras.reverse()
        
        self.vels = [-15.0, -13.0, -11.0, -9.0, -7.0]
        self.vel = 0
        self.grav = 20.5
        self.fim = False
        self.apertou = False

        self.pos = []
        for n in range(5):
            x = 8 + (140 + 8) * n
            y = -290 #(500 - 280) - 50 * n 
            maxy = (500 - 280) - 50 * n
            pos = [x, y, maxy]
            self.pos.append(pos) 
        self.pos.reverse()

    def pular(self,i):
        self.vels[i] = -5

    def draw(self, tela):
        for i,letra in enumerate(self.letras):
            tela.blit(letra, [self.pos[i][0], self.pos[i][1]])

    def update(self, tela, dt):
        for i,pos in enumerate(self.pos):
            self.vels[i] += self.grav * dt
            pos[1] += self.vels[i]
            if pos[1] > randint(pos[2], pos[2] + 100) and not self.apertou:
                self.pular(i)
    
        if self.apertou:
            menor_valor = min(pos[1] for pos in self.pos)
            if menor_valor > 600:
                self.fim = True 

        self.draw(tela)