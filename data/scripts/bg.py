import pygame as pg
from random import randint
class BG:
    def __init__(self):
        self.img = pg.image.load('data/img/nuvem.png').convert_alpha()
        self.pos = [randint(100, 700)+800,randint(100, 400)]
        self.vel = 100
        self.lista = []
        self.lista_criada = False

    def create_list(self):
        if not self.lista_criada:
            for n in range(6):
                img = pg.transform.scale_by(self.img, n)
                pos = [randint(0, 800)+800, randint(0, 600)]
                self.lista.append([img, pos])
            self.lista_criada = True

    def move(self, dt):
        for i, nuvem in enumerate(self.lista):
            valor = self.vel + i*10.5 
            nuvem[1][0] -= valor * dt

            # RESPAWN
            if nuvem[1][0] < 0 - nuvem[0].get_width():
                nuvem[1][0] = randint(100, 700)+800
                nuvem[1][1] = randint(100, 400)

    def draw(self, tela):
        tela.blits(self.lista)

    def update(self, tela, dt):
        self.create_list()
        self.move(dt)
        self.draw(tela)

class GROUND:
    def __init__(self):
        surf = pg.transform.scale_by(pg.image.load('data/img/ground.png').convert_alpha(), 4)
        self.w = surf.get_width()

        self.ground_lista = []
        for n in range(2):
            pos = [0, 500]
            if n == 1:
                pos[0] = 800
            self.ground_lista.append([surf, pos])
        self.vel = 160

    def move(self, dt):
        for n in self.ground_lista:
            n[1][0] -= self.vel * dt
            
            if n[1][0] + self.w <= 0:
                n[1][0] = 800

    def draw(self, tela):
        tela.blits(self.ground_lista)
        
    def update(self, tela, dt):
        self.move(dt)
        self.draw(tela)
        