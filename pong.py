

# PRINTA ARENA

arena = dict()
arena[(0,0)] = '+'
arena[(80,0)] = '+'
arena[(0,20)] = '+'
arena[(80,20)] = '+'

for x in range(1,80):
    arena[(x,0)] = '-'
    arena[(x,20)] = '-'

for y in range(1,20):
    arena[(0,y)] = '|'
    arena[(80,y)] = '|'

def printa_arena():
    for y in range(21):
        linha = ''
        for x in range(81):
            try:
                caractere = arena[(x, y)]
            except KeyError:
                caractere = ' '
            linha += caractere
        print(linha)
            

# RAQUETE

raquete_esq = 10
raquete_dir = 10

def update_raquetes():
    global raquete_esq, raquete_dir

    for y in range(-2,3):
        arena[(2, y + raquete_esq)] = ')'

    for y in range(-2,3):
        arena[(78, y + raquete_dir)] = '('

    arena[(2, raquete_esq + -3)] = ' '
    arena[(2, raquete_esq + 3)] = ' '
    arena[(78, raquete_dir + -3)] = ' '
    arena[(78, raquete_dir + 3)] = ' '

# BOLINHA

bx, by = 40, 10
dirx, diry = 1, 1

def bolinha():
    global bx, by, dirx, diry, JOGO

    arena[(bx, by)] = ' '

    if bx >= 80:
        JOGO = False
    if bx <= 0:
        JOGO = False

    if bx == 77:
        if by in range(raquete_dir - 2, raquete_dir + 3):
            dirx = -1
    if bx == 3:
        if by in range(raquete_esq - 2, raquete_esq + 3):
            dirx = 1

    if by >= 19:
        diry = -1
    if by <= 1:
        diry = 1

    bx = bx + dirx
    by = by + diry

    arena[(bx, by)] = 'O'




import time
import os
import keyboard

JOGO = True
velocidade = 0.03

# JOGO
while JOGO:
    os.system('cls')        
    update_raquetes()
    bolinha()
    printa_arena()
    print()
    print(round(velocidade, 3))
   
    time.sleep(velocidade)
    velocidade = velocidade * 0.999

    if keyboard.is_pressed('w'):
        raquete_esq = raquete_esq - 1
    if keyboard.is_pressed('s'):
        raquete_esq = raquete_esq + 1

    if keyboard.is_pressed('up arrow'):
        raquete_dir = raquete_dir - 1
    if keyboard.is_pressed('down arrow'):
        raquete_dir = raquete_dir + 1
    
    

def move_raquete():
    x = input('mover raquete para:\n')
    if x == 'w':
        print('para cima')
    if x == 's':
        print('para baixo')

#move_raquete()






