"""Jogo do Turtle
File
-------
Turtle.py
-------
    Lucas Feng <lucasfeng@usp.br>
"""

import turtle
import time
import random
from turtle_map import get_map


def init_window():
    """Inicia a janela onde o jogo é executado
    Returns
    -------
    Retorna o  objeto da janela "wn"
    """
    window = turtle.Screen()
    window.title("Turtle Game")
    window.bgcolor("white")
    window.setup(width=600, height=600)
    window.tracer(0)
    return window


def init_turtle():
    """Inicia o objeto que representa a tartaruga líder (head)
    Returns
    -------
    Retorna a variável que representa a tartaruga principal (head)
    """
    head = turtle.Turtle()
    head.speed(0)
    head.shape("turtle")
    head.color("black")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"
    return head


def init_food():
    """Inicia o objeto que representa a comida (bolinha vermelha)
    Returns
    -------
    Retorna o objeto que representa a comida
    """
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0, 100)
    return food


def get_tiltangle(direction):
    """Função para pegar a angulação de uma dada direção
    Parameters
    -------
    direction: string
        Variável que representa a direção do objeto ("right", "left", "up" ou "down")
    Returns
    -------
    Retorna a angulação do objeto
    """
    angle = 0
    if direction == "right":
        angle = 0
    elif direction == "up":
        angle = 90
    elif direction == "left":
        angle = 180
    elif direction == "down":
        angle = 270
    return angle


def change_direction(turtle_object, direction):
    """Função para modificar a direção de um objeto Turtle
    Parameters
    -------
    turtle_object : Turtle
        Variável que representa a tartaruga (seguidora ou líder)
    direction : string
        Variável que representa a direção do objeto ("right", "left", "up" ou "down")
    """
    turtle_object.direction = direction
    turtle_object.tiltangle(get_tiltangle(direction))


def move(head):
    """Função para mover a tartaruga líder dependendo de sua direção
    Parameters
    -------
    head : Turtle
        Variável que representa a tartaruga líder
    """
    if head.direction == "up":
        coordinate_y = head.ycor()
        head.sety(coordinate_y + 20)
    if head.direction == "down":
        coordinate_y = head.ycor()
        head.sety(coordinate_y - 20)
    if head.direction == "left":
        coordinate_x = head.xcor()
        head.setx(coordinate_x - 20)
    if head.direction == "right":
        coordinate_x = head.xcor()
        head.setx(coordinate_x + 20)


def move_segments(segments, head):
    """Função para mover as tartarugas seguidoras de acordo com a tartaruga líder
    Parameters
    -------
    segments : Turtle[]
        Variável que representa as tartarugas seguidoras
    head : Turtle
        Variável que representa a tartaruga líder
    """
    for index in range(len(segments) - 1, 0, -1):
        coordinate_x = segments[index - 1].xcor()
        coordinate_y = segments[index - 1].ycor()
        change_direction(segments[index], segments[index - 1].direction)
        segments[index].goto(coordinate_x, coordinate_y)
    if len(segments) > 0:
        coordinate_x = head.xcor()
        coordinate_y = head.ycor()
        change_direction(segments[0], head.direction)
        segments[0].goto(coordinate_x, coordinate_y)


def setup_keyboard(window, head):
    """Função para preparar a janela para "escutar" o teclado
    Parameters
    -------
    window : Screen
        Objeto que representa a janela
    head : Turtle
        Variável que representa a tartaruga líder
    """

    def go_up():
        """Função para mandar a tartaruga líder se mover para cima"""
        if head.direction != "down":
            change_direction(head, "up")

    def go_down():
        """Função para mandar a tartaruga líder se mover para baixo"""
        if head.direction != "up":
            change_direction(head, "down")

    def go_left():
        """Função para mandar a tartaruga líder se mover para esquerda"""
        if head.direction != "right":
            change_direction(head, "left")

    def go_right():
        """Função para mandar a tartaruga líder se mover para direita"""
        if head.direction != "left":
            change_direction(head, "right")

    window.listen()
    window.onkeypress(go_up, "w")
    window.onkeypress(go_down, "s")
    window.onkeypress(go_left, "a")
    window.onkeypress(go_right, "d")

    """Uma opção caso a tecla CAPS LOCK esteja ativada"""
    window.onkeypress(go_up, "W")
    window.onkeypress(go_down, "S")
    window.onkeypress(go_left, "A")
    window.onkeypress(go_right, "D")


def is_turtle_off_screen(head):
    """Função que devolve se a tartaruga está dentro ou fora da janela
    Parameters
    -------
    head : Turtle
        Objeto que representa a tartaruga líder
    Returns
    -------
    Uma variável booleana que indica se a tartaruga está dentro ou fora da janela
    """
    return (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    )


def is_turtle_head_on_body(head, segments):
    """Função que devolve se a tartaruga líder está colidindo com uma de suas seguidoras
    Parameters
    -------
    head : Turtle
        Objeto que representa a tartaruga líder
    segments : Turtle[]
        Objeto que representa as tartarugas seguidoras
    Returns
    -------
    Uma variável booleana que indica se a tartaruga líder está colidindo com uma de suas seguidoras
    """
    for segment in segments:
        if segment.distance(head) < 20:
            return True
    return False


def respawn_food(food, blocks):
    """Função que reposiciona o alimento da tartaruga
    Parameters
    -------
    food : Turtle
        Objeto que representa a comida
        blocks : Turtle []
        Objetos que representam os obstáculos do mapa
    """
    is_food_unreachable = True
    while is_food_unreachable:
        coordinate_x = random.randint(-290, 290)
        coordinate_y = random.randint(-290, 290)
        is_food_unreachable = False
        for block in blocks:
            if block.distance(coordinate_x, coordinate_y) < 20:
                is_food_unreachable = True
                break
    food.goto(coordinate_x, coordinate_y)


def hide_segments(segments):
    """Função que faz desaparecer as tartarugas seguidoras
    Parameters
    -------
    segments : Turtle[]
        Objeto que representam as tartarugas seguidoras
    """
    for segment in segments:
        segment.hideturtle()
    segments.clear()


def add_turtle_segment(segments):
    """Função que adiciona uma tartaruga às tartarugas seguidoras
    Parameters
    -------
    segments : Turtle[]
        Objeto que representam as tartarugas seguidoras
    """
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape("turtle")
    new_segment.color("black")
    new_segment.penup()
    segments.append(new_segment)


def reset_turtle(head):
    """Função que "reseta" o posicionamento da tartaruga líder
    Parameters
    -------
    head : Turtle
        Objeto que representam a tartaruga líder
    """
    head.goto(0, 0)
    head.direction = "stop"


def build_block(coordinate_x, coordinate_y):
    """Função responsável por criar um obstáculo nas coordenadas coordinate_x e coordinate_y
    Parameters
    -------
    coordinate_x : int
        Coordenada horizontal no plano cartesiano
    coordinate_y : int
        Coordenada vertical no plano cartesiano
    Returns
    -------
    Retorna o obstáculo individual que foi criado
    """
    block = turtle.Turtle()
    block.speed(0)
    block.shape("square")
    block.color("black")
    block.penup()
    block.goto(coordinate_x * 20 - 300, 300 - coordinate_y * 20)
    return block


def build_map(obstacle_map):
    """Função responsável por receber uma matriz de char e criar os obstáculos do mapa
    Parameters
    -------
    obstacle_map : char[][]
        Matriz com as informações dos obstáculos do mapa
    Returns
    -------
    Retorna um vetor com todos os obstáculos criados
    """
    blocks = []
    coordinate_y = 0
    for row in obstacle_map:
        coordinate_x = 0
        for char in row:
            if char == "#":
                block = build_block(coordinate_x, coordinate_y)
                blocks.append(block)
            coordinate_x += 1
        coordinate_y += 1
    return blocks


def is_turtle_head_colliding(head, blocks):
    """Função que avalia se a tartaruga líder colidiu com um obstáculo do mapa
    Parameters
    -------
    head : Turtle
        Objeto que representa a tartaruga líder
    blocks : Turtle[]
        Vetor de objetos que representam os obstáculos do mapa
    Returns
    -------
    Retorna verdadeiro se a tartaruga líder colidiu
    """
    for block in blocks:
        if block.distance(head) < 20:
            return True
    return False


def main():
    """Função principal, que define o ciclo do jogo"""
    delay_value = 0.1
    ### Será deixado para ser implementado como tarefinha
    print("Bem vindo ao Turtle!")
    while True:
        print("Escolha entre as dificuldades Facil Medio e Dificil")
        difficulty = input("Dificuldade desejada: ")
        if difficulty in ('Facil', 'facil'):
            delay_value = 0.1
            break
        if difficulty in ('Medio', 'medio'):
            delay_value = 0.075
            break
        if difficulty in ('Dificil', 'dificil'):
            delay_value = 0.05
            break
        print("Dificuldade inválida, tente de novo \n")

    obstacle_map = get_map()
    blocks = build_map(obstacle_map)
    window = init_window()
    head = init_turtle()
    food = init_food()
    setup_keyboard(window, head)
    segments = []
    delay = delay_value

    while True:
        window.update()

        if is_turtle_off_screen(head):
            time.sleep(1)
            reset_turtle(head)
            hide_segments(segments)
            delay = delay_value

        if head.distance(food) < 20:
            respawn_food(food, blocks)
            add_turtle_segment(segments)
            delay -= 0.001

        move_segments(segments, head)
        move(head)

        if is_turtle_head_on_body(head, segments) or is_turtle_head_colliding(
            head, blocks
        ):
            time.sleep(1)
            reset_turtle(head)
            hide_segments(segments)
            delay = delay_value

        time.sleep(delay)


# Função main
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, turtle.Terminator) as e:
        print("\nFalou, até!")