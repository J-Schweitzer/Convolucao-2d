import numpy as np
import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from filters import filters

custom_filter_window = None  # Definindo custom_filter_window como uma variável global
entries = []  # Definindo entries como uma variável global
filtered_image = None  # Variável para armazenar a imagem filtrada

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
        kernel = filters[selected_filter]

        print("Núcleo de convolução: ")
        print(kernel)

        kernel_label.config(text="Núcleo de convolução: \n" + str(kernel))
        create_custom_filter_window()
    else:
        # Obtém o kernel do filtro selecionado
        kernel = filters[selected_filter]

        print("Núcleo de convolução: ")
        print(kernel)

        kernel_label.config(text="Núcleo de convolução: \n" + str(kernel))

        # Aplica a convolução à imagem em escala de cinza
        global filtered_image
        filtered_image = convolution(imagem_suavizada, kernel)

        # Exibe a imagem resultante
        plt.imshow(filtered_image, cmap='gray')
        plt.axis('off')
        plt.show()

def apply_filter_custom():
    # Verifica se entries não é None
    if entries:
        # Obtém os valores da matriz do filtro personalizado dos campos de entrada
        custom_filter = [[float(entry.get()) for entry in row] for row in entries]

        # Converte a imagem original para escala de cinza
        imagem_cinza = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        imagem_suavizada = smooth_image(imagem_cinza)

        # Aplica a convolução à imagem em escala de cinza usando o filtro personalizado
        global filtered_image
        filtered_image = convolution(imagem_suavizada, np.array(custom_filter))

        # Exibe a imagem resultante
        plt.imshow(filtered_image, cmap='gray')
        plt.axis('off')
        plt.show()

    else:
        print("Nenhuma matriz de filtro personalizado foi criada.")

def create_custom_filter_window():
    global custom_filter_window, entries, dim_entry_row, dim_entry_col

    custom_filter_window = tk.Toplevel(root)
    custom_filter_window.title("Matriz do Filtro Personalizado")

    # Etapa 1: Entrada para o número de linhas
    tk.Label(custom_filter_window, text="Número de Linhas:").grid(row=0, column=0)
    dim_entry_row = tk.Entry(custom_filter_window, width=5)
    dim_entry_row.grid(row=0, column=1)
    
    # Etapa 2: Entrada para o número de colunas
    tk.Label(custom_filter_window, text="Número de Colunas:").grid(row=1, column=0)
    dim_entry_col = tk.Entry(custom_filter_window, width=5)
    dim_entry_col.grid(row=1, column=1)

    # Botão para confirmar a dimensão da matriz
    confirm_button = tk.Button(custom_filter_window, text="Confirmar", command=confirm_dimension)
    confirm_button.grid(row=2, columnspan=2, pady=10)

def confirm_dimension():
    # Obter o número de linhas e colunas inseridas pelo usuário
    num_rows = int(dim_entry_row.get())
    num_cols = int(dim_entry_col.get())

    # Criar a janela para a matriz do filtro
    create_filter_matrix_window(num_rows, num_cols)

def create_filter_matrix_window(num_rows, num_cols):
    global custom_filter_window, entries

    if custom_filter_window:
        custom_filter_window.destroy()

    custom_filter_window = tk.Toplevel(root)
    custom_filter_window.title("Matriz do Filtro Personalizado")

    entries = []
    for i in range(num_rows):
        row_entries = []
        for j in range(num_cols):
            entry = tk.Entry(custom_filter_window, width=5)
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        entries.append(row_entries)

    # Botão para aplicar o filtro personalizado
    apply_button_custom = tk.Button(custom_filter_window, text="Aplicar Filtro Personalizado", command=apply_filter_custom)
    apply_button_custom.grid(row=num_rows, columnspan=num_cols, pady=10)


# Função para salvar a imagem filtrada
def save_filtered_image():
    global filtered_image
    if filtered_image is not None:
        save_image(filtered_image)
    else:
        print("Nenhuma imagem filtrada disponível para salvar.")

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

# Cria uma lista suspensa para selecionar o filtro
filter_variable = tk.StringVar(root)
filter_variable.set(list(filters.keys())[0])  # Define o filtro padrão

filter_dropdown = tk.OptionMenu(root, filter_variable, *filters.keys())
filter_dropdown.pack(pady=10)

kernel_label = tk.Label(root, text = "Núcleo de Convolução: ")
kernel_label.pack(pady=5)

# Cria um botão para aplicar o filtro
apply_button = tk.Button(root, text="Aplicar Filtro", command=apply_filter)
apply_button.pack(pady=10)

# Criar um botão para o usuário aplicar um filtro personalizado
custom_filter_button = tk.Button(root, text="Filtro Personalizado", command=create_custom_filter_window)
custom_filter_button.pack(pady=10)

# Cria um botão para salvar a imagem filtrada
save_button = tk.Button(root, text="Salvar Imagem", command=save_filtered_image)
save_button.pack(pady=10)

# Executa o loop principal da aplicação
root.mainloop()
