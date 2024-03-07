import pygame as pg
from sys import exit  
pg.init()

from settings import tela, clock, debug_fps

from data.scripts.player import BIRD
from data.scripts.cenario import CANO, BG, GROUND
from data.scripts.hud import TITLE, BARRA, PONTOS
from data.scripts.particulas import PARTICLES

bg = BG()
ch = GROUND()
cano = CANO() 
bird = BIRD()  
titulo = TITLE()
pontos = PONTOS()
barra = BARRA()
part = PARTICLES()

class JOGO:
    def __init__(self):
        self.cena_atual = 'intro'
        self.gameloop = True

    def Intro(self):
        tela.fill((63, 93, 251))
        dt = clock.tick(144)/1000.0

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.gameloop = False #fecha janela do jogo

            if ev.type == pg.KEYDOWN: 
                if ev.key == pg.K_SPACE:
                    titulo.fim = True
                    if not titulo.anim: #animação do titulo
                        if not bird.anim: #animação do bird
                            barra.estado = 'gameplay'
                            bird.apertou_space = True
                            self.cena_atual = 'game'

        self.UpdateEvents(dt)
        pg.display.flip()
        clock.tick()
    def Game(self): 
        tela.fill((63, 93, 251))
        dt = clock.tick(144)/1000.0

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.gameloop = False

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    bird.pulo()
                    part.pulo(bird.pos)

        self.CollisionEvents(dt)
        self.UpdateEvents(dt)
        pg.display.flip()
        clock.tick()
    def GameOver(self):
        tela.fill((63, 93, 251))
        dt = clock.tick(144)/1000.0

        for ev in pg.event.get():
            if ev.type == pg.QUIT: 
                self.gameloop = False
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    if bird.pos[1] > 600 and cano.lista[0]['rect'].x < 0 - cano.w:
                        #restart bird stats
                        bird.pos = [0 - 32, 200 - 32]
                        bird.vel = 0
                        bird.f_impacto = 0
                        bird.grav = 20.5
                        bird.estado = 'respawn'
                        bird.bateu = False
                        bird.anim = False
                        # RESTART WORLD STAT
                        ch.vel = 160
                        bg.vel = 100
                        cano.vel = 150
                        cano.movery = False
                        part.dir_x = 1
                        part.q_sangue = 0
                        part.q_cair = 4
                        part.raio = 11
                        part.morreu = True

                        pontos.modo = 'reset'
                        pontos.numero = 0
                        self.cena_atual = 'game'
                        
                        barra.estado = 'gameplay'

        self.UpdateEvents(dt)
        self.CollisionEvents(dt)
        pg.display.flip()

    def UpdateEvents(self, dt):
        if self.cena_atual == 'intro':#---------INTRO
            bg.update(tela, dt)
            ch.update(tela, dt)

            if titulo.anim: #ANIMAÇÃO DO TITULO
                titulo.update(tela, dt) 
            else: 
                part.rastro(bird.pos)
                part.update(tela)

                bird.estado = 'tutorial'
                bird.update(tela, dt, cano.rectlist) 

                barra.estado = 'tutorial'
                barra.update(tela, dt)

        elif self.cena_atual == 'game':#---------GAME
            bg.update(tela, dt)  
            part.update(tela)
            cano.update(tela, dt)
            if not bird.estado == 'respawn':
                bird.estado = 'gameplay'
            bird.update(tela, dt, cano.rectlist)
            ch.update(tela, dt) 
            pontos.update(tela, dt)
            barra.update(tela, dt)

        elif self.cena_atual == 'game over':#---GAME OVER
            bg.update(tela, dt)   
            cano.update(tela, dt)
            bird.update(tela, dt, cano.rectlist)
            part.update(tela)
            ch.update(tela, dt) 
            pontos.update(tela, dt)
            barra.update(tela, dt)
    
    def CollisionEvents(self, dt):
        if self.cena_atual == 'game':#---------GAME
            if bird.bateu:
                bird.estado = 'game over'
                self.cena_atual = 'game over'

            # CANO PASSOU NA TELA E ESTA X = 0 (RESET DO CANO)
            if cano.lista[0]['rect'].x <= 0 - cano.w:
                cano.respawn() 

                # aumentar a velocidade      
                n = 5
                for ev in [bg, cano, ch]:
                    ev.vel += 20 + n
                    n += 5 

                if cano.movery == True:
                    if cano.vel_y > 0:
                        cano.vel_y += 10
                    if cano.vel_y < 0:
                        cano.vel_y -= 10

                # Status do bird e particulas aumentam
                bird.upgrade_stats()
                part.upgrade_stats()

            # AUMENTAR PONTOS QUANDO BIRD ESTIVER ALINHADO COM CANO
            if cano.lista[0]['rect'].x < bird.pos[0]:
                if not bird.passou:
                    pontos.numero += 1
                    pontos.outline = True
                    bird.passou = True
            else:
                bird.passou = False

            # CASO VELOCIDADE DO CANO FOR >= 40 
            if cano.vel >= 400:
                cano.moveY(dt) # função q mexe o y dos canos

            # COLISÕES DO BIRD (CHAO E TETO)
            if bird.pos[1] > 600 - 32:
                bird.estado = 'game over'
                self.cena_atual = 'game over'

            elif bird.pos[1] < 0 - 100:
                bird.estado = 'game over'
                self.cena_atual = 'game over'

        elif self.cena_atual == 'game over':#--GAME OVER
            pontos.modo = 'animação'
            barra.estado = 'tutorial'

            if bird.pos[1] > 600 - 32:
                part.cair(bird.pos)

            if not cano.lista[0]['rect'].x <= 0 - cano.w:
                for obj in [bg, cano, ch]:
                    obj.vel += 0.4
            else:
                for obj in [bg, cano, ch]:
                    if obj.vel > 0:
                        obj.vel -= 0.4
                    bird.estado = 'game over'

    def GerenciadorCenas(self):
        if self.cena_atual == 'intro':
            self.Intro()

        if self.cena_atual == 'game':
            clock.tick()
            self.Game()

        if self.cena_atual == 'game over':
            clock.tick()
            self.GameOver()

jogo = JOGO()
gameloop = True
while gameloop:
    jogo.GerenciadorCenas()
    gameloop = jogo.gameloop
pg.quit()
exit()