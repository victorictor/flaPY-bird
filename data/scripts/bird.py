import pygame as pg

class BIRD:
    def __init__(self):
        sheet = pg.transform.scale_by(pg.image.load('data/img/bird.png'),4).convert_alpha()
        
        self.frame = [
            sheet.subsurface((0,0, 64, 36)),
            sheet.subsurface((64,0, 64, 36)),
            sheet.subsurface((128,0, 64, 36))
            ]
        
        self.framecount = 0
        self.index = 0
        self.surf = self.frame[0]

        self.pos = [200 - 32, 300 - 32]
        self.vel = 0
        self.grav = 20.5
        self.peso = 0.5

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

    def pulo(self, dt):
        self.vel = -5 
    
    def colisao(self, rectlist):
        self.rect = pg.rect.FRect(self.pos, self.surf.get_size())
        if self.rect.collidelist(rectlist) != -1:
            pass
        else:
            pass

    def draw(self, tela):
        tela.blit(self.surf, self.pos)

    def update(self, tela, dt, rectlist, cena):
        self.vel += self.grav * dt
        self.pos[1] += self.vel
        
        self.animation(cena)
        self.colisao(rectlist)
        self.draw(tela)