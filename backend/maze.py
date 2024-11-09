import random
import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import io
import base64
import time
import copy

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  

labirinto_atual = None

BRANCO = [255, 255, 255]
PRETO = [0, 0, 0]
VERDE = [0, 255, 0]
VERMELHO = [255, 0, 0]

def eh_branco(pixel):
    return [255, 255, 255] == pixel

def eh_verde(pixel):
    return pixel == [0, 255, 0]


def mostrar_caminho(adj, pais, start, tam):
    key = start[0] * tam + start[1]

    while key != tam:
        idx = pais[key]

        adj[idx[0]][idx[1]] = [204, 153, 0]

        key = idx[0] * tam + idx[1]

        emit('receive_matrix', {'image': adj})
        socketio.sleep(0.005)
    
    

def bfs(adj):
    q = deque()
    pais = dict()
    curr = []

    tam = len(adj[0])

    q.append([1,0])

    while q:
        curr = q.popleft()
        
        el = adj[curr[0]][curr[1]]

        adj[curr[0]][curr[1]] = VERMELHO[:]


        emit('receive_matrix', {'image': adj})
        socketio.sleep(0.005)

        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            res = [x + y for x, y in zip(curr, i)]
            
            el = adj[res[0]][res[1]]

            if el == VERDE:
                pais[res[0] * tam + res[1]] = curr
                mostrar_caminho(adj, pais, res, tam)
                return

            if res[0] < len(adj) and res[0] > 0:
                pass
            else:
                continue

            if res[1] < len(adj[0]) and res[1] > 0:
                pass
            else:
                continue

            if el == BRANCO:
                pais[res[0] * tam + res[1]] = curr
                q.append(res)



def dfs(adj):
    q = deque()
    pais = dict()
    curr = [1,0]

    tam = len(adj[0])
    
    q.append([1,0])
    adj[curr[0]][curr[1]] = VERMELHO[:]


    while q:

        curr = q.pop()
        el = adj[curr[0]][curr[1]]

        emit('receive_matrix', {'image': adj})
        socketio.sleep(0.005)
      

        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            res = [x + y for x, y in zip(curr, i)]
            el = adj[res[0]][res[1]]

            if el == VERDE:
                pais[res[0] * tam + res[1]] = curr
                mostrar_caminho(adj, pais, res, tam)
                return

            if res[0] < len(adj) and res[0] > 0:
                pass
            else:
                continue

            if res[1] < len(adj[0]) and res[1] > 0:
                pass
            else:
                continue

            if el == BRANCO:
                pais[res[0] * tam + res[1]] = curr
                adj[curr[0]][curr[1]] = [255, 0, 0]
                #curr = res
                q.append(curr)
                q.append(res)
                break
        else:
            #curr = q.pop()
            adj[curr[0]][curr[1]] = [34, 90, 34]
            emit('receive_matrix', {'image': adj})
            socketio.sleep(0.005)




def remover_paredes_aleatorias(labirinto, num_paredes):
    largura, altura = len(labirinto[0]), len(labirinto)
    paredes_removidas = 0
    while paredes_removidas < num_paredes:
        x = random.randrange(1, largura - 1)
        y = random.randrange(1, altura - 1)
        if labirinto[y][x] == PRETO and labirinto[y][x - 1] == PRETO and labirinto[y][x + 1] == PRETO and not(labirinto[y + 1][x] == PRETO or labirinto[y - 1][x] == PRETO):
            labirinto[y][x] = BRANCO
            emit('receive_labirinto', {'image': labirinto})
            socketio.sleep(0.005)
            paredes_removidas += 1
        elif labirinto[y][x] == PRETO and labirinto[y - 1][x] == PRETO and labirinto[y + 1][x] == PRETO and not(labirinto[y][x - 1] == PRETO or labirinto[y][x + 1] == PRETO):
            labirinto[y][x] = BRANCO
            emit('receive_labirinto', {'image': labirinto})
            socketio.sleep(0.005)
            paredes_removidas += 1

def e_par(largura, altura):
    if(largura % 2 == 0):
        largura = largura + 1

    if(altura % 2 == 0):
        altura = altura + 1
    return [largura, altura]


def gerar_labirinto(largura, altura, paredes):

    largura, altura = e_par(largura, altura)

    labirinto = [[PRETO]* largura for _ in range(altura)]

    def eh_valido(x, y):
        return 0 <= x < largura and 0 <= y < altura

    def dfs(x, y):
        labirinto[y][x] = BRANCO[:]

        emit('receive_labirinto', {'image': labirinto})
        socketio.sleep(0.005)

        direcoes = [(0, 2), (2, 0), (0, -2), (-2, 0)]  
        random.shuffle(direcoes)

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if eh_valido(nx, ny) and labirinto[ny][nx] == PRETO:
                labirinto[y + dy // 2][x + dx // 2] = BRANCO[:]

                emit('receive_labirinto', {'image': labirinto})
                socketio.sleep(0.005)
                dfs(nx, ny)

    dfs(1, 1)
    labirinto[1][0] = BRANCO[:]
    labirinto[-2][-1] = VERDE[:]

    emit('receive_labirinto', {'image': labirinto})
    socketio.sleep(0.005)

    remover_paredes_aleatorias(labirinto, paredes)
    
    return labirinto


@socketio.on('send_matrix')
def solucao(data):
    try:
        algorithm = data.get('algorithm')
        copia = copy.deepcopy(labirinto_atual)
        if algorithm == 'bfs':
            bfs(copia)
        elif algorithm == 'dfs':
            dfs(copia)
        else:
            print("Algoritmo inválido, deve ser 'bfs' ou 'dfs'.")
            
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        socketio.emit('error', {'message': 'Falha ao processar a imagem.'})


@socketio.on('send_labirinto')
def gera_labirinto(data):
    global labirinto_atual
    try:
        largura = data.get('largura')
        altura = data.get('altura')
        paredes = data.get('paredes')

        labirinto_atual = gerar_labirinto(largura, altura, paredes)
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        socketio.emit('error', {'message': 'Falha ao processar a imagem.'})



if __name__ == '__main__':
    socketio.run(app, debug=True)
