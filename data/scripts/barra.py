import pygame as pg

class BARRA:
    def __init__(s):
        sheet = pg.transform.scale_by(pg.image.load('data/img/barra_sheet.png'), 4)
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