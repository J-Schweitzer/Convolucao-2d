import numpy as np

# Definindo os filtros
filters = {
    'Filtro Suavizacao por Media': np.ones((5, 5)) / 25,
 
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