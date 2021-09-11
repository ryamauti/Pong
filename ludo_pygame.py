import pygame
import json
import random

EM_JOGO = True
CFG = {'WIDTH': 1000, 'HEIGHT': 740, 'MARGEM_ESQ': 250, 'MARGEM_SUP': 50, 'TAMANHO_CEL': 40}
INGAME = {'STATUS': 'vazio', 'DADO': 0, 'JOGADOR': 'verde'}
CORES = {'black': (0,0,0), 'white': (255,255,255), 'gray': (127,127,127), 'light_gray': (192,192,192),
         'green': (0,255,0), 'red': (255,0,0), 'blue': (0,0,255), 'yellow': (255,255,0)}


selected_rect = None

with open("ludo_campo.json", "r") as f:
    dados_ludo = json.loads(f.read()) 

pygame.init()
screen = pygame.display.set_mode((CFG['WIDTH'], CFG['HEIGHT']))

clock = pygame.time.Clock()

## FUNCOES DO JOGO

def preenche_campos(dados, i):    
    px = dados[i]['x']
    py = dados[i]['y']
    x = CFG['MARGEM_ESQ'] + CFG['TAMANHO_CEL']*px
    y = CFG['MARGEM_SUP'] + CFG['TAMANHO_CEL']*py
    return x, y

def quad(x, y, tam, cor):
    pygame.draw.rect(screen, CORES[cor], pygame.Rect(x-tam//2, y-tam//2, tam, tam), 5)   

def circ(x, y, tam, cor):
    pygame.draw.circle(screen, CORES[cor], (x, y), tam, 5)   

def pawn(x, y, tam, cor):
    pygame.draw.polygon(screen, CORES[cor], points=[(x-tam//3, y+tam//3), (x, y-tam//2), (x+tam//3, y+tam//3)])
    collider = pygame.Rect(x-tam//2, y-tam//2, tam, tam)
    return collider

def distancia(t1, t2):
    tam = CFG['TAMANHO_CEL']//2
    if (t1[0] - t2[0]) ** 2 + (t1[1] - t2[1]) ** 2 < tam ** 2:
        return True
    else:
        return False


## TABULEIRO 
def atualiza_tabuleiro():
    tamanho = CFG['TAMANHO_CEL']

    for cores in dados_ludo:
        neutro = 'gray'
        cor = dados_ludo[cores]['cor']

        campo = dados_ludo[cores]['campo']
        for i in campo:
            x, y = preenche_campos(campo, i)
            quad(x, y, tamanho, neutro)

        campo = dados_ludo[cores]['seguro']
        for i in campo:
            x, y = preenche_campos(campo, i)
            quad(x, y, tamanho, cor)

        campo = dados_ludo[cores]['centro']
        for i in campo:
            x, y = preenche_campos(campo, i)
            circ(x, y, tamanho*2.5, cor)
        
        campo = dados_ludo[cores]['casa']
        for i in campo:
            x, y = preenche_campos(campo, i)
            quad(x, y, tamanho, neutro)

        campo = dados_ludo[cores]['peoes']
        for i in campo:
            x, y = preenche_campos(campo, i)
            pawn(x, y, tamanho, cor)
            dados_ludo[cores]['peoes'][i]['centro'] = (x, y)            


def checa_clique(pos_mouse):
    for cores in dados_ludo:
        campo = dados_ludo[cores]['peoes']
        for i in campo:
            pos_peao = dados_ludo[cores]['peoes'][i]['centro']
            if distancia(pos_peao, pos_mouse):
                print(i)
                print(dados_ludo[cores]['peoes'][i])


def checa_casas(player):
    campo = dados_ludo[player]['peoes']
    rua = 0
    casa = 0
    for i in campo:
        local = dados_ludo[player]['peoes'][i]['status']
        if local == 'rua':
            rua += 1
        if local == 'casa':
            casa += 1
    print(rua, casa)
            


## LAÇO DO JOGO
## ------------

#pre-fill
screen.fill(CORES['light_gray'])
atualiza_tabuleiro()

screen.blit(pygame.font.SysFont('Calibri', 30).render('Jogo de Ludo!', True, CORES['black']), (30, 30))
screen.blit(pygame.font.SysFont('Calibri', 20).render('Para iniciar clique abaixo', True, CORES['black']), (30, 80))

btn_rect = pygame.draw.rect(screen, CORES['gray'], pygame.Rect(30, 300, 180, 130))
screen.blit(pygame.font.SysFont('Calibri', 30).render('Iniciar jogo', True, CORES['black']), (50, 350))
btn_hover = False 

pygame.display.update()

pygame.display.flip()



while EM_JOGO:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EM_JOGO = False
        
        if event.type == pygame.MOUSEMOTION:            
            if btn_rect.collidepoint(pygame.mouse.get_pos()) and btn_hover == False:
                pygame.draw.rect(screen, (100,100,100), pygame.Rect(30, 300, 180, 130), 20)
                screen.blit(pygame.font.SysFont('Calibri', 30).render('Iniciar jogo', True, CORES['black']), (50, 350))
                btn_hover = True
                pygame.display.flip()

            if btn_hover == True and btn_rect.collidepoint(pygame.mouse.get_pos()) == 0:
                btn_rect = pygame.draw.rect(screen, (127,127,127), pygame.Rect(30, 300, 180, 130))
                screen.blit(pygame.font.SysFont('Calibri', 30).render('Iniciar jogo', True, CORES['black']), (50, 350))
                btn_hover = False
                pygame.display.flip()

        left, middle, right = pygame.mouse.get_pressed()
        if left:
            checa_clique(pygame.mouse.get_pos())
        if right:
            checa_casas('verde')
            
    

    clock.tick(60)