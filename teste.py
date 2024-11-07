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

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  

def eh_branco(pixel):
    return [255, 255, 255] == pixel

def eh_verde(pixel):
    return pixel == [0, 255, 0]

def imagem_para_base64(imagem):
    buffered = io.BytesIO()
    imagem.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str



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
        curr = q.pop()
        
        el = adj[curr[0]][curr[1]]

        adj[curr[0]][curr[1]] = [255, 0, 0]


        emit('receive_matrix', {'image': adj})
        socketio.sleep(0.005)

        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            res = [x + y for x, y in zip(curr, i)]
            
            el = adj[res[0]][res[1]]

            if eh_verde([el[0], el[1], el[2]]):
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

            if eh_branco([el[0], el[1], el[2]]):
                pais[res[0] * tam + res[1]] = curr
                q.append(res)



def dfs(adj):
    q = deque()
    pais = dict()
    curr = [1,0]

    tam = len(adj[0])
    
    q.append([1,0])
    adj[curr[0]][curr[1]] = [255, 0, 0]


    while q:
        
        el = adj[curr[0]][curr[1]]

        emit('receive_matrix', {'image': adj})
        socketio.sleep(0.005)
      

        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            res = [x + y for x, y in zip(curr, i)]
            el = adj[res[0]][res[1]]

            if eh_verde([el[0], el[1], el[2]]):
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

            if eh_branco([el[0], el[1], el[2]]):
                pais[res[0] * tam + res[1]] = curr
                adj[curr[0]][curr[1]] = [255, 0, 0]
                curr = res
                q.append(res)
                break
        else:
            curr = q.pop()
            adj[curr[0]][curr[1]] = [34, 90, 34]




@socketio.on('send_matrix')
def solucao(data):
    try:
        image_array = data['image']
        algorithm = data.get('algorithm')

        if algorithm == 'bfs':
            bfs(image_array)
        elif algorithm == 'dfs':
            dfs(image_array)
        else:
            print("Algoritmo inválido, deve ser 'bfs' ou 'dfs'.")
            
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        socketio.emit('error', {'message': 'Falha ao processar a imagem.'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
