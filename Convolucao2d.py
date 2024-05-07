import numpy as np
import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

def convolution(image, kernel):
    # Obtém as dimensões da imagem e do kernel
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape

    # Calcula o padding necessário para que a saída tenha o mesmo tamanho da imagem original
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    # Aplica o padding na imagem original
    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')

    # Cria uma matriz para armazenar o resultado da convolução
    output = np.zeros_like(image)

    # Aplica a convolução
    for i in range(image_height):
        for j in range(image_width):
            # Multiplica os elementos da região da imagem pelo kernel e soma o resultado
            output[i, j] = np.sum(padded_image[i:i+kernel_height, j:j+kernel_width] * kernel)

    return output


def load_image():

    # Abre uma janela de diálogo para selecionar um arquivo de imagem
    file_path = filedialog.askopenfilename()

    # Carrega a imagem selecionada usando OpenCV
    global original_image
    original_image = cv2.imread(file_path)

    # Convertendo a imagem para tons de cinza
    imagem_cinza = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)


    # Mostra a imagem original
    cv2.imshow("Original Image", imagem_cinza)
    cv2.waitKey(0)

def apply_filter():
    imagem_suavizada = convolution(original_image, filters['Filtro Suavizacao por Media 21'])

    # Obtém o filtro selecionado
    selected_filter = filter_variable.get()

    # Obtém o kernel do filtro selecionado
    kernel = filters[selected_filter]

    # Aplica a convolução à imagem carregada
    output_image = convolution(imagem_suavizada, kernel)

    # Mostra a imagem resultante
    plt.imshow(output_image, cmap='gray')
    plt.axis('off')
    plt.show()


# Cria uma instância da janela principal
root = tk.Tk()
root.title("Aplicação de Filtros")

# Define as dimensões da janela
window_width = 300
window_height = 150
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Configura a janela para ser fixa
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.resizable(False, False)  # Desativa o redimensionamento

# Cria um botão para carregar a imagem
load_button = tk.Button(root, text="Carregar Imagem", command=load_image)
load_button.pack(pady=10)

# Definindo os filtros
filters = {
    'Filtro Suavizacao por Media': np.ones((5, 5)) / 25,

    'Filtro Suavizacao por Media 21': np.ones((21, 21)) / 441,


    'Suavização por Mediana': np.array([[1, 1, 1, 1, 1],
                                          [1, 1, 1, 1, 1],
                                          [1, 1, 1, 1, 1],
                                          [1, 1, 1, 1, 1],
                                          [1, 1, 1, 1, 1]], dtype=np.float32) / 25,

    'Filtro Laplaciano' : np.array([[0,  0, -1,  0,  0],
                                  [0, -1, -2, -1,  0],
                                  [-1, -2, 16, -2, -1],
                                  [0, -1, -2, -1,  0],
                                  [0,  0, -1,  0,  0]]),

    'Filtro Gaussiano' : np.array([[1,  4,  7,  4, 1],
                                 [4, 16, 26, 16, 4],
                                 [7, 26, 41, 26, 7],
                                 [4, 16, 26, 16, 4],
                                 [1,  4,  7,  4, 1]]) / 273,
    
    'Filtro de Nitidez' : np.array([[-1, -1, -1, -1, -1],
                               [-1,  2,  2,  2, -1],
                               [-1,  2,  8,  2, -1],
                               [-1,  2,  2,  2, -1],
                               [-1, -1, -1, -1, -1]]),

    'Filtro Emboss' : np.array([[-2, -1,  0,  1,  2],
                              [-1, -1,  0,  1,  1],
                              [-1,  0,  0,  0,  1],
                              [-1, -1,  0,  1,  1],
                              [-2, -1,  0,  1,  2]]),

    'Filtro Sobel Vertical' : np.array([[-1, -2,  0,  2,  1],
                                      [-2, -3,  0,  3,  2],
                                      [-4, -6,  0,  6,  4],
                                      [-2, -3,  0,  3,  2],
                                      [-1, -2,  0,  2,  1]]),

    'Filtro Sobel Horizontal' : np.array([[-1, -2, -1],
                                        [0, 0, 0,],
                                        [1,  2,  1],]),

    'Sharpen': np.array([[0, 0, -1, 0, 0],
                                              [0, -1, -2, -1, 0],
                                              [-1, -2, 20, -2, -1],
                                              [0, -1, -2, -1, 0],
                                              [0, 0, -1, 0, 0]], dtype=np.float32)
}

# Cria uma lista suspensa para selecionar o filtro
filter_variable = tk.StringVar(root)
filter_variable.set(list(filters.keys())[0])  # Define o filtro padrão

filter_dropdown = tk.OptionMenu(root, filter_variable, *filters.keys())
filter_dropdown.pack(pady=10)

# Cria um botão para aplicar o filtro
apply_button = tk.Button(root, text="Aplicar Filtro", command=apply_filter)
apply_button.pack(pady=10)

# Executa o loop principal da aplicação
root.mainloop()