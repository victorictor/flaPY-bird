import pygame as pg

class PONTOS:
    def __init__(self):
        self.font = pg.font.Font('data/img/Daydream.ttf', 100)

        self.numero = 0
        self.cor = (115, 134, 228) #(172, 185, 251)
        self.img = self.font.render(str(self.numero), True, self.cor)
        self.outlines = []

        self.size = self.img.get_size()
        self.pos = [800 - (self.size[0] + 20), 0 + 20]
        self.vel = 500
        self.modo = 'normal'
        self.restart = True
        self.outline = True

    def get_outline(self, img, pos):
        mask = pg.mask.from_surface(img)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey((0,0,0))
        for px in range(mask_surf.get_width()):
            for py in range(mask_surf.get_height()):
                if mask_surf.get_at((px, py)) == (255, 255, 255):
                    mask_surf.set_at((px, py), self.cor)
        self.outlines = []
        self.outlines.append([mask_surf, [pos[0]-10, pos[1]]])
        self.outlines.append([mask_surf, [pos[0]+10, pos[1]]])
        self.outlines.append([mask_surf, [pos[0], pos[1]-10]])
        self.outlines.append([mask_surf, [pos[0], pos[1]+10]])   
    
    def normal(self):
        self.img = self.font.render(str(self.numero), True, (251, 251, 251)).convert_alpha()
        self.size = self.img.get_size()
        self.pos = [800 - (self.size[0] + 20), 0 + 20]

        if self.restart:
            self.outline = True
            self.restart = False

    def anim(self, dt):
        if self.pos[0] >= 400 - self.size[0]//2:
            self.pos[0] -= self.vel * dt
            self.pos[1] += self.vel//2 * dt
            for outline in self.outlines:
                outline[1][0] -= self.vel * dt
                outline[1][1] += self.vel//2 * dt

    def reset(self, dt):
        if self.pos[0] < 800 - (self.size[0] + 20):
            self.pos[0] += self.vel * dt
            self.pos[1] -= self.vel//2 * dt
            for outline in self.outlines:
                outline[1][0] += self.vel * dt
                outline[1][1] -= self.vel//2 * dt
        else:
            self.numero = 0
            self.outline = True
            self.img = self.font.render(str(self.numero), True, (251, 251, 251)).convert_alpha()  
            self.modo = 'normal'
            self.restart = True
            
    def draw(self, tela):
        tela.blits(self.outlines)
        tela.blit(self.img, self.pos)

    def update(self, tela, dt):
        if self.modo == 'normal':
            self.normal()
        elif self.modo == 'animação':
            self.anim(dt)
        elif self.modo == 'reset':
            self.reset(dt)

        if self.outline:
            self.get_outline(self.img, self.pos)
            self.outline = False

        self.draw(tela)
