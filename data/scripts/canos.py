import pygame as pg
from random import randint

class CANO:
    def __init__(self):
        self.surf = pg.transform.scale_by(pg.image.load('data/img/cano.png'), 4).convert_alpha()
        w, h = self.surf.get_size()
        ry = randint(100, 500)
        
        self.dif =  200
        self.vel = 150
        self.dif_y = lambda n : n - h - self.dif

        self.rectlist = []
        self.cano = [{'img': self.surf, 
                      'rect': pg.rect.FRect(800, ry, w, h)},

                     {'img': pg.transform.flip(self.surf, False, True), 
                      'rect': pg.rect.FRect(800, self.dif_y(ry), w, h)}]
        
    def move(self, dt):
        for cano in self.cano:
            cano['rect'].x -= self.vel * dt
            
    def respawn(self):
        ry = randint(100, 500)
        if self.cano[0]['rect'].x <= 0 - self.surf.get_width():
            for i, cano in enumerate(self.cano):
                cano['rect'].x = 800
                if i == 0:
                    cano['rect'].y = ry
                else:
                    cano['rect'].y = self.dif_y(ry)

    def atualizar_rect(self):
        self.rectlist.clear()
        for n in range(2):
            rect = self.cano[n]['rect']
            self.rectlist.append(rect)
    
    def draw(self, tela):
        for cano in self.cano:
            tela.blit(cano['img'], cano['rect'])

    def update(self, tela, dt):
        self.move(dt)
        self.respawn()
        self.atualizar_rect()
        self.draw(tela)
        