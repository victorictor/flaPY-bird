import pygame as pg
from sys import exit  

from data.scripts.bird import BIRD
from data.scripts.canos import CANO
from data.scripts.bg import BG, GROUND
from data.scripts.title import TITLE
from data.scripts.particulas import PARTICLES
from data.scripts.pontos import PONTOS
from data.scripts.barra import BARRA

pg.init()

tela = pg.display.set_mode((800, 600)) 
clock = pg.time.Clock()
G = 9.807

bg = BG()
ch = GROUND()
bird = BIRD()  
cano = CANO() 
titulo = TITLE()
p = PARTICLES()
pontos = PONTOS()
barra = BARRA()

class JOGO:
    def __init__(self):
        self.cena_atual = 'menu'

    def intro(self):
        dt = clock.tick(144)/1000.0

        if titulo.fim:
            barra.estado = 'tutorial'

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                exit()
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    titulo.apertou = True
                    if titulo.fim:
                        if bird.pode_apertar:
                            barra.estado = 'gameplay'
                            bird.apertou_space = True
                            self.cena_atual = 'game'

        tela.fill((63, 93, 251))
        bg.update(tela, dt)
        ch.update(tela, dt)

        titulo.update(tela, dt)
        p.update(tela)
        barra.update(tela, dt)
    

        if titulo.fim:
            bird.estado = 'tutorial'
            p.rastro(bird.pos)
            p.update(tela)
            bird.update(tela, dt, cano.rectlist, self.cena_atual)   

        pg.display.flip()
        clock.tick()

    def game(self): 
        if bird.bateu:
            cano.bird_morto = True
            bird.estado = 'game over'
            self.cena_atual = "game over"

        tela.fill((63, 93, 251))
        
        dt = clock.tick(144)/1000.0
        for obj in pg.event.get():
            if obj.type == pg.QUIT:
                quit()

            if obj.type == pg.KEYDOWN:
                if obj.key == pg.K_SPACE:
                    bird.pulo()
                    p.pulo(bird.pos)

        bg.update(tela, dt)  
        p.update(tela)
        cano.update(tela, dt)
        if not bird.estado == 'respawn':
            bird.estado = 'gameplay'
        bird.update(tela, dt, cano.rectlist, self.cena_atual)
        ch.update(tela, dt) 
        pontos.update(tela, dt)
        barra.update(tela, dt)

        if cano.cano_list[0]['rect'].x <= 0 - cano.w:
            cano.respawn()       
            n = 5
            for obj in [bg, cano, ch]:
                obj.vel += 20 + n
                n += 5
            if cano.movery == True:
                if cano.vel_y > 0:
                    cano.vel_y += 10
                    
                if cano.vel_y < 0:
                    cano.vel_y -= 10
                
            bird.f_impacto += 0.1
            bird.grav += 0.1
            p.dir_x += 0.3
            p.q_sangue += 1
            p.q_cair += 1

        if cano.cano_list[0]['rect'].x < bird.pos[0]:
            if not bird.passou:
                pontos.numero += 1
                pontos.outline = True
                bird.passou = True
        else:
            bird.passou = False

        if cano.vel >= 400:
            cano.moveY(dt)

        if bird.pos[1] > 600 - 32:
            bird.estado = 'game over'
            self.cena_atual = 'game over'

        elif bird.pos[1] < 0 - 100:
            bird.estado = 'game over'
            self.cena_atual = 'game over'

        pg.display.flip()
        clock.tick()

    def game_over(self):
        tela.fill((63, 93, 251))
        dt = clock.tick(144)/1000.0
        bird.estado = 'game over'
        pontos.modo = 'animação'
        barra.estado = 'tutorial'

        for ev in pg.event.get():
            if ev.type == pg.QUIT: 
                quit()
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    if bird.pos[1] > 600 and cano.cano_list[0]['rect'].x < 0 - cano.w:
                        #restart bird stats
                        bird.pos = [0 - 32, 200 - 32]
                        bird.vel = 0
                        bird.f_impacto = 0
                        bird.grav = 20.5
                        bird.estado = 'respawn'
                        bird.bateu = False
                        bird.pode_apertar = False
                        # RESTART WORLD STAT
                        ch.vel = 160
                        bg.vel = 100
                        cano.vel = 150
                        cano.movery = False
                        p.dir_x = 1
                        p.q_sangue = 0
                        p.q_cair = 4
                        p.raio = 11
                        p.morreu = True

                        pontos.modo = 'reset'
                        pontos.numero = 0
                        self.cena_atual = 'game'
                        
                        barra.estado = 'gameplay'

        if bird.pos[1] > 600 - 32:
            p.cair(bird.pos)

        if not cano.cano_list[0]['rect'].x <= 0 - cano.w:
            for obj in [bg, cano, ch]:
                obj.vel += 0.4
        else:
            for obj in [bg, cano, ch]:
                if obj.vel > 0:
                    obj.vel -= 0.4

        bg.update(tela, dt)   
        cano.update(tela, dt)
        bird.update(tela, dt, cano.rectlist, self.cena_atual)
        p.update(tela)
        ch.update(tela, dt) 
        pontos.update(tela, dt)
        barra.update(tela, dt)
        pg.display.flip()

    def trocar_cena(self):
        if self.cena_atual == 'menu':
            self.intro()

        if self.cena_atual == 'game':
            clock.tick()
            self.game()

        if self.cena_atual == 'game over':
            clock.tick()
            self.game_over()

cenas = JOGO()
while True:
    cenas.trocar_cena()