import pygame as pg

# o powerup vai diminuir a velocidade e a força da gravidade no bird
# o powerup vai ter uma chance de aparacer de segundos e segundos
class POWERUP:
    def __init__(self):
        self.surf = pg.transform.scale_by(pg.image.load('data/img/powerup.png'), 4)
        self.pos = [900, 100]
        self.vel = 150

    def move(self, dt):
        self.pos[1] += 100 * dt
        self.pos[0] -= 250 * dt

    def draw(self, tela):
        tela.blit(self.surf, self.pos)

    def update(self, tela, dt):
        self.move(dt)
        self.draw(tela)