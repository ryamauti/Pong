import turtle

s = turtle.getscreen()
t = turtle.Turtle()


def poligono(lados, tamanho=100):
    for _ in range(lados):
        t.forward(tamanho)
        t.left(360 / lados)

poligono(4, tamanho=100)
t.left(90)
poligono(4, tamanho=120)
t.left(90)
poligono(4, tamanho=140)
t.left(90)
poligono(4, tamanho=160)



input('pressione ENTER para encerrar')