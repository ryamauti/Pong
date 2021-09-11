import tkinter as tk
import json
import random

margem_esq = 150
margem_sup = 40
tamanho = 40

JOGADOR = 'verde'
EM_JOGO = True
STATUS = 'vazio'
DADO = 0

with open("ludo_campo.json", "r") as f:
    dados_ludo = json.loads(f.read()) 


def iniciar():
    atualiza_tabuleiro()
    jogo_1_dados()


win = tk.Tk()

canvas = tk.Canvas(win, width=1200, height=800)
canvas.pack()

label1 = tk.Label(canvas, text="")
canvas.create_window(10, 120, anchor=tk.W, window=label1)

button1 = tk.Button(canvas, text="", command =iniciar)
canvas.create_window(10, 200, anchor=tk.W, window=button1)

label2 = tk.Label(canvas, text="")
canvas.create_window(10, 240, anchor=tk.W, window=label2)



def circ(x, y, tam, cor):
    canvas.create_oval(x-tam//2, y-tam//2, x+tam//2, y+tam//2, fill=cor)

def quad(x, y, tam, cor):
    canvas.create_rectangle(x-tam//2, y-tam//2, x+tam//2, y+tam//2, fill=cor)

def draw_pawn(x, y, tam, cor, tag):
    sprite = canvas.create_polygon( x-tam//3, y+tam//3, 
                                    x, y-tam//2, 
                                    x+tam//3, y+tam//3, 
                                    fill=cor, outline='black',
                                    tags=('peao', cor, tag))
    return sprite


def sprite_click(event):
    global STATUS, JOGADOR    

    if STATUS == 'mover peao':
        # <ButtonPress event state=Mod1 num=1 x=717 y=602>    
        item = canvas.find_closest(event.x, event.y)    
        taglist = canvas.gettags(*item)
        
        if taglist[0] == 'peao':
            # checar se é sua vez
            if taglist[2][:-2] == JOGADOR:
                selecionado = taglist[2]
                info_peao = dados_ludo[JOGADOR]['peoes'][selecionado]               
                logica(selecionado)
    

def preenche_campos(dados, i):    
    px = dados[i]['x']
    py = dados[i]['y']
    x = margem_esq + tamanho*px
    y = margem_sup + tamanho*py
    return x, y

## TABULEIRO 
def atualiza_tabuleiro():
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
            circ(x, y, tamanho*5, cor)
        
        campo = dados_ludo[cores]['casa']
        for i in campo:
            x, y = preenche_campos(campo, i)
            quad(x, y, tamanho, neutro)

        ## PEOES   
        campo = dados_ludo[cores]['peoes']
        for i in campo:
            tag = dados_ludo[cores]['peoes'][i]['tag']
            x, y = preenche_campos(campo, i)
            sprite = draw_pawn(x, y, tamanho, cor, tag) 
            canvas.tag_bind(sprite, "<Button-1>", sprite_click)


## INICIO
STATUS = 'inicio'
label1.config(text = "LUDO. Para iniciar\nclique abaixo")
button1.config(text = "Iniciar")


def rodar_dado():
    dado = random.randint(1, 6)
    print(dado)
    jogo_2_move(dado)


## VEZ DO JOGADOR
## RODAR DADO
def jogo_1_dados(novamente=''):  
    global STATUS, DADO
    STATUS = 'rodar dado'
    DADO = 0
    label1.config(text = "Vez do {0}".format(JOGADOR))
    label2.config(text = "{0}, favor\nlançar o dado{1}".format(JOGADOR, novamente))
    button1.config(text = "Rolar dado", state = tk.NORMAL, command =rodar_dado)
    

## ESCOLHER PEAO A MOVER
def jogo_2_move(valor):
    global STATUS, DADO
    DADO = valor
    STATUS = 'mover peao'
    label2.config(text = "{0}, você tirou {1}.\nfavor escolher o peao.".format(JOGADOR, str(valor)))
    button1.config(text = "-->", state = tk.DISABLED)

## ENCERRAR O TURNO
def jogo_3_proximo(proximo):
    global STATUS, JOGADOR    
    STATUS = 'finalizar'
    JOGADOR = proximo
    jogo_1_dados()


## LOGICA DO LUDO
def logica(selecionado):
    global DADO
    JOGADOR = selecionado[:-2]

    ### Se o peao está na casa, apenas o número 1 e 6 o liberta   
    if dados_ludo[JOGADOR]['peoes'][selecionado]['status'] == 'casa':
        saida = dados_ludo[JOGADOR]['campo']['1']
        if DADO == 1 or DADO == 6:
            dados_ludo[JOGADOR]['peoes'][selecionado]['x'] == saida['x']
            dados_ludo[JOGADOR]['peoes'][selecionado]['y'] == saida['y']
            dados_ludo[JOGADOR]['peoes'][selecionado]['status'] == 'rua'
            print(dados_ludo[JOGADOR]['peoes'][selecionado])
            atualiza_tabuleiro()

        if DADO == 1:
            jogo_3_proximo(dados_ludo[JOGADOR]['proximo'])

        if DADO == 6:            
            jogo_1_dados(' novamente')



    
win.mainloop()

