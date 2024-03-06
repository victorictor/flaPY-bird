from pygame import font, mask, transform, image, Surface
from random import randint
class PONTOS:
    def __init__(self):
        self.font = font.Font('data/img/hud/Daydream.ttf', 100)

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
        mas = mask.from_surface(img)
        mask_surf = mas.to_surface()
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

class TITLE:
    def __init__(self):
        sheet = transform.scale_by(image.load('data/img/hud/flapy.png').convert_alpha(), 4)
        cut_pos = [
            (0, 0, 37, 70),
            (37, 0, 36, 59),
            (73, 0, 51, 68), 
            (124, 0, 41, 64),
            (165, 0, 46, 70)]

        cot_pos_x4 = [(x*4, y*4, w*4, h*4) for (x,y,w,h) in cut_pos]
        self.letras = [Surface.subsurface(sheet, rect) for rect in cot_pos_x4]
        self.letras.reverse()
        
        self.vels = [-15.0, -13.0, -11.0, -9.0, -7.0]
        self.vel = 0
        self.grav = 20.5
        self.anim = True
        self.fim = False

        self.pos = []
        for n in range(5):
            x = 8 + (140 + 8) * n
            y = -290 
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
        # GRAVIDADE NAS LETRAS
        for i,pos in enumerate(self.pos):
            self.vels[i] += self.grav * dt
            pos[1] += self.vels[i]

            # FAZER LETRAS PULAREM
            if not self.fim:
                if pos[1] > randint(pos[2], pos[2] + 100):
                    self.pular(i)

            # FAZER LETRAS CAIREM(FIM DA ANIMAÇÃO)
            elif self.fim:
                menor_valor = min(pos[1] for pos in self.pos) #pegar ultima letra a cair 
                if menor_valor > 600:
                    self.anim = False
        self.draw(tela)

class BARRA:
    def __init__(s):
        sheet = transform.scale_by(image.load('data/img/hud/barra_sheet.png'), 4)
        s.frame = [sheet.subsurface(0, 0, 368, 112), 
                   sheet.subsurface(372, 0, 368, 112)]
        
        s.surf = s.frame[1]
        s.size = s.surf.get_size()
        s.pos = [800, 400]
        s.posy = s.pos[1]

        s.estado = 'parado'

        s.framecount = 0
        s.index = 0
        s.valor = [1, 1]    
        s.vel = 600

    def frame_change(s):
        s.framecount = (s.framecount + 1)%30
        if s.framecount == 0:
            s.index = (s.index + 1) %2
            
        s.surf = s.frame[s.index]
    
    def anim(s, dt):
        s.pos[1] += s.valor[1]
        if s.pos[1] < s.posy - 10:
            s.valor[1] = 10 * dt
        elif s.pos[1] > s.posy + 10:
            s.valor[1] = -10 * dt
        '''
        s.pos[0] += s.valor[0]
        if s.pos[0] < 200 - 10:
            s.valor[0] = 10 * dt
        elif s.pos[0] > 200 + 10:
            s.valor[0] = -10 * dt'''
    
    def move(s, dt):
        if s.estado == 'tutorial':
            s.anim(dt)
            if s.pos[0] > 800/2 - s.size[0]//2:
                s.pos[0] -= s.vel * dt

        if s.estado == 'gameplay':
            s.pos[0] -= s.vel * dt

    def draw(s, tela):
        tela.blit(s.surf, s.pos)

    def update(s, tela, dt):
        s.frame_change()
        s.move(dt)
        
        # RESPAWN
        if s.pos[0] < 0 - s.size[0]:
            s.estado = 'parado'
            s.pos =  [800, 400]

        s.draw(tela)