from pygame import transform, image, rect
from random import randint
class CANO:
    def __init__(self):
        self.surf = transform.scale_by(image.load('data/img/cenario/cano.png'), 4).convert_alpha()
        w, h = self.surf.get_size()
        self.w = w
        ry = randint(100, 500)
        
        self.dif =  200
        self.vel = 150
        self.vel_y = 150
        self.dif_y = lambda n : n - h - self.dif
        self.movery = False

        self.rectlist = []
        self.lista = [{'img': self.surf, 
                      'rect': rect.FRect(800, ry, w, h)},

                     {'img': transform.flip(self.surf, False, True), 
                      'rect': rect.FRect(800, self.dif_y(ry), w, h)}]
        
    def move(self, dt):
        for cano in self.lista:
            cano['rect'].x -= self.vel * dt

    def moveY(self, dt):
        self.movery = True
        for i, cano in enumerate(self.lista):
            if i == 0:
                if cano['rect'].y > 500:
                    self.vel_y *= -1

                if cano['rect'].y < 100 + self.dif:
                    self.vel_y = abs(self.vel_y)

            cano['rect'].y += self.vel_y * dt
    
    def respawn(self):
        ry = randint(100, 500)
        if self.lista[0]['rect'].x <= 0 - self.w:
            for i, cano in enumerate(self.lista):
                cano['rect'].x = 800
                if i == 0:
                    cano['rect'].y = ry
                else:
                    cano['rect'].y = self.dif_y(ry)

    def atualizar_rect(self):
        self.rectlist.clear()
        for n in range(2):
            rect = self.lista[n]['rect']
            self.rectlist.append(rect)
    
    def draw(self, tela):
        for cano in self.lista:
            tela.blit(cano['img'], cano['rect'])

    def update(self, tela, dt):
        self.move(dt)
        self.atualizar_rect()
        self.draw(tela)

class BG:
    def __init__(self):
        self.img = image.load('data/img/cenario/nuvem.png').convert_alpha()
        self.pos = [randint(100, 700)+800,randint(100, 400)]
        self.vel = 100
        self.lista = []
        self.lista_criada = False

    def create_list(self):
        if not self.lista_criada:
            for n in range(6):
                img = transform.scale_by(self.img, n)
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
        surf = transform.scale_by(image.load('data/img/cenario/ground.png').convert_alpha(), 4)
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