import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
