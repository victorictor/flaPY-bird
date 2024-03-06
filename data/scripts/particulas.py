import pygame as pg
from random import randint, uniform

class PARTICLES:
    def __init__(self):
        self.partula_lista = []
        self.cor = (251, 251, 251)

        self.pos = [100, 100]
        self.raio = 11
        self.dir_x = 1
        self.q_sangue = 2
        self.q_cair = 4
        
        self.framecount = 0

        self.gerar_particula = False
        self.morreu = True

    def pulo(self, pos):
        pos = int(pos[0] +32), int(pos[1]+32)
        for _ in range(10):
            pos = [randint(pos[0] - 10, pos[0] + 10), 
                randint(pos[1] - 5, pos[1] + 5)]
            Dir = [ self.dir_x, -1]

            part_stats = [pos, self.raio, Dir, 'pulo', 0.1, (251, 251, 251)]
            self.partula_lista.append(part_stats)

    def rastro(self, pos):
        pos = int(pos[0] + 32//2), int(pos[1] + 32)
        self.framecount = (self.framecount + 1)%30
        if self.framecount == 0:
            for _ in range(3):
                pos = [randint(pos[0]- 5, pos[0] + 5), 
                    randint(pos[1] - 10, pos[1] + 10)]
                Dir = [1, 0]

                part_stats = [pos, self.raio, Dir, 'rastro', 0.1, (251, 251, 251)]
                self.partula_lista.append(part_stats)

    def impacto(self, pos):
        pos = int(pos[0]), int(pos[1])
        self.framecount = (self.framecount + 1)%30
        if self.framecount == 0:
            for _ in range(self.q_sangue):
                pos = [randint(pos[0] - 2, pos[0] + 2),
                        randint(pos[1] - 2, pos[1] + 2)]
                Dir = [randint(1, 3),
                        randint(-3, 3)]

                part_stats = [pos, self.raio, Dir, 'impacto', 0.3, 'red']
                self.partula_lista.append(part_stats)

    def cair(self, pos):
        pos = int(pos[0]), int(pos[1])
        if self.morreu:
            for _ in range(self.q_cair):
                pos = [randint(pos[0] - 10, pos[0] + 10),
                    randint(pos[1] - 20, pos[1] + 20)]
                
                Dir = [uniform(-1, self.dir_x),
                    self.dir_x]

                part_stats = [pos, self.raio, Dir, 'cair', 0.1, (251, 251, 251)]
                self.partula_lista.append(part_stats)
            self.morreu = False
    def deletar(self):
        self.partula_lista = [p for p in self.partula_lista if p[1] > 0]

    def draw(self, tela):        
        for p in self.partula_lista:
            if p[1] <= 7 and p[5] == (251, 251, 251):
                p[5] = (172, 185, 251)

            p[0][0] -= p[2][0]
            p[0][1] -= p[2][1]
            p[1] -= p[4]

            pg.draw.circle(tela, p[5], p[0], int(p[1]))

    def update(self, tela):
        self.draw(tela)
        self.deletar()
