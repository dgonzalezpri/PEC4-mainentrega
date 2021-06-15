"""" Este módulo provee de las funcionalidades necesarias para pintar gráficamente dataframes
"""

import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def plot_bar_chart(dataframe):
    """" Esta funcion recibe un dataframe como entrada y pinta un gráfico de barras

    :param dataframe: (Dataframe): el dataframe a visualizar
    """
    dataframe.plot.bar()
    plt.show()
