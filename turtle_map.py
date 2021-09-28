import os


def get_map():
    """Função que lê o arquivo 'map.txt' e devolve uma matriz de caracteres

    Returns
    -------
    Retorna uma matriz de caracteres que representam o mapa do jogo
    """
    here = os.path.dirname(os.path.abspath(__file__))

    filename = os.path.join(here, "map.txt")
    file = open(filename)
    map = file.read()

    line = []
    map_result = []

    for char in map:
        if char != "\n":
            line.append(char)
        else:
            map_result.append(line.copy())
            line.clear()

    map_result.append(line.copy())
    return map_result
