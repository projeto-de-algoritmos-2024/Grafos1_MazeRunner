import random
import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

BRANCO = [255, 255, 255]
PRETO = [0, 0, 0]
VERDE = [0, 255, 0]

def e_par(largura, altura):
    if(largura % 2 == 0):
        largura = largura + 1

    if(altura % 2 == 0):
        altura = altura + 1
    return [largura, altura]


def gerar_labirinto(largura, altura):

    largura, altura = e_par(largura, altura)

    labirinto = [[PRETO]* largura for _ in range(altura)]

    def eh_valido(x, y):
        return 0 <= x < largura and 0 <= y < altura

    def dfs(x, y):
        labirinto[y][x] = BRANCO

        plt.clf()

        plt.imshow(labirinto)
        plt.axis('off')
        plt.pause(0.00005)

        direcoes = [(0, 2), (2, 0), (0, -2), (-2, 0)]  
        random.shuffle(direcoes)

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if eh_valido(nx, ny) and labirinto[ny][nx] == PRETO:
                labirinto[y + dy // 2][x + dx // 2] = BRANCO

                plt.clf()

                plt.imshow(labirinto)
                plt.axis('off')
                plt.pause(0.00005)
                dfs(nx, ny)

    dfs(1, 1)
    labirinto[1][0] = BRANCO
    labirinto[-2][-1] = VERDE

    plt.imshow(labirinto)
    plt.axis('off')
    plt.pause(0.00005)
    
    return labirinto


def remover_paredes_aleatorias(labirinto, num_paredes):
    largura, altura = len(labirinto[0]), len(labirinto)
    paredes_removidas = 0
    while paredes_removidas < num_paredes:
        x = random.randrange(1, largura - 1)
        y = random.randrange(1, altura - 1)
        if labirinto[y][x] == PRETO and labirinto[y][x - 1] == PRETO and labirinto[y][x + 1] == PRETO and not(labirinto[y + 1][x] == PRETO or labirinto[y - 1][x] == PRETO):
            labirinto[y][x] = BRANCO
            plt.imshow(labirinto)
            plt.axis('off')
            plt.pause(0.00005)
            paredes_removidas += 1
        elif labirinto[y][x] == PRETO and labirinto[y - 1][x] == PRETO and labirinto[y + 1][x] == PRETO and not(labirinto[y][x - 1] == PRETO or labirinto[y][x + 1] == PRETO):
            labirinto[y][x] = BRANCO
            plt.imshow(labirinto)
            plt.axis('off')
            plt.pause(0.00005)
            paredes_removidas += 1


largura, altura = 20, 20  
labirinto = gerar_labirinto(largura, altura)

remover_paredes_aleatorias(labirinto, 11)


# Convert the maze to an image and save it as PNG
img = Image.fromarray(np.array(labirinto, dtype=np.uint8))
img = img.convert("RGB")
width, height = img.size
img.save("labirinto_final.png")

plt.ioff()
plt.show()


