import pygame as pg
from random import uniform, randint
class BIRD:
    def __init__(self):
        sheet = pg.transform.scale_by(pg.image.load('data/img/bird.png'),4).convert_alpha()
        
        self.frame = [
            sheet.subsurface((0,0, 64, 36)),
            sheet.subsurface((64,0, 64, 36)),
            sheet.subsurface((128,0, 64, 36)),
            sheet.subsurface((192,0, 64, 36))
            ]
        
        self.framecount = 0
        self.index = 0
        self.surf = self.frame[0]
        self.dead_surf = self.frame[3]
        
        #self.pos = [200 - 32, 300 - 32]
        self.pos = [0 - 32, 300 - 32]
        self.posy = self.pos[1]
        self.vel = 0
        self.grav = 20.5
        self.peso = 0.5
        self.f_impacto = 2
        self.valor = 1
        self.valorx = 1

        self.bateu = False
        self.angle = 0
        self.offset = 0
        self.apertou_space = False
        self.pode_apertar = False
        self.passou = False

        self.estado = 'tutorial'
        self.rect = pg.rect.FRect(self.pos, self.surf.get_size())

    def animation(self, cena):
        if cena == 'menu':
            self.framecount = (self.framecount + 1) % 15
            if self.framecount == 0 :
                self.index = (self.index + 1) % 3
            self.surf = self.frame[self.index]

        else:
            self.framecount = (self.framecount + 1) % 15
            if self.framecount == 0 :
                if self.vel < 0:
                    self.index = (self.index + 1) % 3
                else:
                    self.index = 0
                self.surf = self.frame[self.index]

    def tutorial_anim(self, dt):
        if self.pos[0] < 200 - 32:
            self.pos[0] += 200 * dt

        self.pos[1] += self.valor 
        if self.pos[1] < self.posy - 10:
            self.valor = 10 * dt
        if self.pos[1] > self.posy + 10:
            self.valor = -10 * dt

        self.pos[0] += self.valorx
        if self.pos[0] < 200 -10:
            self.valorx = 10 * dt
        if self.pos[0] > 200 +10:
            self.valorx = -10 * dt
        
        if 170 < self.pos[0] < 200:
            self.pode_apertar = True

    def respawn_anim(self):
        if self.pos[0] < 200 - 32:
            self.pos[0] += 5
        else:
            self.pode_apertar = True
            self.estado = 'gameplay'

    def morte_anim(self):
        self.pos[0] += uniform(self.f_impacto, self.f_impacto + 2)
        self.pos[1] -= uniform(self.f_impacto, self.f_impacto + 2)

        self.framecount = (self.framecount + 1) % 15
        if self.framecount == 0:
            self.angle += 90
            self.dead_surf = pg.transform.rotate(self.dead_surf, self.angle)

    def pulo(self):
        if not self.bateu:
            self.vel = -5 

    def colisao(self, rectlist):
        self.rect = pg.rect.FRect(self.pos, self.surf.get_size())
        if self.rect.collidelist(rectlist) != -1:
            self.bateu = True

    def draw(self, tela):
        if self.estado == 'tutorial' or self.estado == 'gameplay':
            tela.blit(self.surf, self.pos)
        else:
            tela.blit(self.dead_surf, self.pos)

    def update(self, tela, dt, rectlist, cena):
        if not self.estado == 'tutorial':
            self.vel += self.grav * dt
            self.pos[1] += self.vel

        if self.estado == 'tutorial':
            self.tutorial_anim(dt)
            self.animation(cena)

            if self.apertou_space:
                self.pulo()

        if self.estado == 'respawn':
            self.respawn_anim()

        if self.estado == 'gameplay':
            self.animation(cena)
            self.colisao(rectlist)
            
        if self.estado == 'game over':
            self.morte_anim()
        
        self.draw(tela)