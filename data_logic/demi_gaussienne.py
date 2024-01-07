import numpy as np
import matplotlib.pyplot as plt

def draw_membership_function(m1, m2, std_gauche, std_droite):
    """
    Trace la gaussienne en fonction de la moyenne et l'ecart type à gauche et à droite
    Notation Left-Right
    paramètres :
        m1 (float) : point gauche du support
        m2 (float) : point droit du support
        std_gauche (float) : l'ecart type à gauche
        std_droite (float) : l'ecart type à droite
    Attention : n'affiche pas le plot. il faut suivre la fonction de plt.show()
    """
    x1 = np.linspace(m1 - 3*std_gauche, m1, 500)
    x2 = np.linspace(m1, m2, 100)
    x3 = np.linspace(m2, m2 + 3*std_droite, 500)
    x = np.concatenate((x1, x2, x3))

    y1 = np.exp(-(x1 - m1)**2 / (2 * std_gauche**2)) if std_gauche > 0 else np.zeros(500)
    y2 = np.ones(100)
    y3 = np.exp(-(x3 - m2)**2 / (2 * std_droite**2)) if std_droite > 0 else np.zeros(500)
    y = np.concatenate((y1, y2, y3))

    plt.plot(x, y)
    plt.show()

if __name__ == "__main__":
    draw_membership_function(100, 110, 0, 50)