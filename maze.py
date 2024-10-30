import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def eh_preto(pixel):
    return [0, 0, 0] == pixel

def eh_branco(pixel):
    return [255, 255, 255] == pixel

def eh_vermelho(pixel):
    return [255, 0, 0] == pixel

def eh_verde(pixel):
    return pixel == [0, 255, 0]


def bfs(adj):
    q = deque();

    q.append([1,0])

    while q:
        curr = q.popleft()
        
        el = adj[curr[0]][curr[1]]

        adj[curr[0]][curr[1]] = [255, 0, 0]

        plt.imshow(adj)
        plt.axis('off')
        plt.pause(0.005)

        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            res = [x + y for x, y in zip(curr, i)]
            print(res)
            print(adj[res[0]][res[1]])
            el = adj[res[0]][res[1]]

            if eh_verde([el[0], el[1], el[2]]):
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
                q.append(res)

        print(q)

     

def main():
    if len(sys.argv) < 2:
        print("Uso: python maze.py maze.png")
        sys.exit(1)

    image = Image.open(sys.argv[1]).convert('RGB')
    
    image_array = np.array(image)
    
    image_array[-2][-1] = [0, 255, 0]

    plt.ion()

    plt.figure(figsize=(5, 5))
    plt.imshow(image_array)
    plt.axis('off')

    bfs(image_array)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
