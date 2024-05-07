import numpy as np
import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

custom_filter_window = None  # Definindo custom_filter_window como uma variável global
entries = None  # Definindo entries como uma variável global

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

def smooth_image(image):
    # Aplica um filtro de suavização (média) à imagem
    kernel = np.ones((5, 5)) / 25  # Filtro de média 5x5
    smoothed_image = convolution(image, kernel)
    return smoothed_image

def load_image():

    # Abre uma janela de diálogo para selecionar um arquivo de imagem
    file_path = filedialog.askopenfilename()

    # Carrega a imagem selecionada usando OpenCV
    global original_image
    original_image = cv2.imread(file_path)

    # Convertendo a imagem para tons de cinza
    imagem_suavizada = smooth_image(cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY))

    # Mostra a imagem original
    plt.imshow(imagem_suavizada, cmap='gray')
    plt.axis('off')
    plt.show()

def save_image(image):
    # Abre uma janela de diálogo para selecionar o local de salvamento da imagem
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg")

    # Verifica se um arquivo foi selecionado
    if file_path:
        # Salva a imagem no local especificado
        cv2.imwrite(file_path, image)
        print("Imagem salva com sucesso!")

def apply_filter():
    # Converte a imagem original para escala de cinza
    imagem_cinza = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    imagem_suavizada = smooth_image(imagem_cinza)

    # Obtém o filtro selecionado
    selected_filter = filter_variable.get()

    if selected_filter == "Custom":
        # Pede ao usuário para inserir a matriz do filtro manualmente
        create_custom_filter_window()
    else:
        # Obtém o kernel do filtro selecionado
        kernel = filters[selected_filter]

        # Aplica a convolução à imagem em escala de cinza
        imagem_filtrada = convolution(imagem_suavizada, kernel)

        # Exibe a imagem resultante
        plt.imshow(imagem_filtrada, cmap='gray')
        plt.axis('off')
        plt.show()

        #save_image(imagem_filtrada)

def apply_filter_custom():
    # Obtém os valores da matriz do filtro personalizado dos campos de entrada
    custom_filter = [[float(entry.get()) for entry in row] for row in entries]

    # Converte a imagem original para escala de cinza
    imagem_cinza = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    imagem_suavizada = smooth_image(imagem_cinza)

    # Aplica a convolução à imagem em escala de cinza usando o filtro personalizado
    imagem_filtrada = convolution(imagem_suavizada, np.array(custom_filter))

    # Exibe a imagem resultante
    plt.imshow(imagem_filtrada, cmap='gray')
    plt.axis('off')
    plt.show()

    #save_image(imagem_filtrada)

#função para criar uma janela e que permite ao usuário inserir uma matriz
def create_custom_filter_window():
    global custom_filter_window, entries

    custom_filter_window = tk.Toplevel(root)
    custom_filter_window.title("Matriz do Filtro Personalizado")

    entries = []
    for i in range(3):
        row_entries = []
        for j in range(3):
            entry = tk.Entry(custom_filter_window, width=5)
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        entries.append(row_entries)

    apply_button = tk.Button(custom_filter_window, text="Aplicar Filtro Personalizado", command=apply_filter_custom)
    apply_button.pack(pady=10)

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

# Cria um botão para carregar a imagem
load_button = tk.Button(root, text="Carregar Imagem", command=load_image)
load_button.pack(pady=10)

# Definindo os filtros
filters = {
    'Filtro Suavizacao por Media': np.ones((5, 5)) / 25,

    'Filtro Suavizacao por Media 21': np.ones((21, 21)) / 441,
 
    'Filtro Laplaciano' : np.array([[0, -1, 0],
                                    [-1, 4, -1],
                                    [0, -1, 0]]),

    'Filtro Gaussiano' : np.array([[1, 2, 1],
                                   [2, 4, 2],
                                   [1, 2, 1]]) / 16,
    
    'Filtro de Nitidez' : np.array([[0, -1, 0],
                                    [-1, 5, -1],
                                    [0, -1, 0]]),

    'Filtro Emboss' : np.array([[-2, -1,  0],
                                [-1,  1,  1],
                                [ 0,  1,  2]]),

    'Filtro Sobel Vertical' : np.array([[-1, 0, 1],
                                        [-2, 0, 2],
                                        [-1, 0, 1]]),

    'Filtro Sobel Horizontal' : np.array([[-1, -2, -1],
                                          [0, 0, 0],
                                          [1, 2, 1]])
}

# Cria uma lista suspensa para selecionar o filtro
filter_variable = tk.StringVar(root)
filter_variable.set(list(filters.keys())[0])  # Define o filtro padrão

filter_dropdown = tk.OptionMenu(root, filter_variable, *filters.keys())
filter_dropdown.pack(pady=10)

# Cria um botão para aplicar o filtro
apply_button = tk.Button(custom_filter_window, text="Aplicar Filtro", command=apply_filter_custom)
apply_button.pack(pady=10)

#Criar um botão para o usuário aplicar um filtro
custom_filter_button = tk.Button(root, text="Filtro Personalizado", command= create_custom_filter_window)
custom_filter_button.pack(pady=10)

# Executa o loop principal da aplicação
root.mainloop()