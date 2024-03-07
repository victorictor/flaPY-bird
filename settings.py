import pygame as pg
LARGURA, ALTURA = 800, 600
tela = pg.display.set_mode((LARGURA, ALTURA)) 
clock = pg.time.Clock()

font = pg.font.SysFont(None, 30)
def debug_fps(tela, fps):
    fps = font.render(str(fps), False, 'black')
    tela.blit(fps, (10,10))