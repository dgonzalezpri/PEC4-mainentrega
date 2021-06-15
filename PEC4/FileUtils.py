"""" Ayuda en operaciones con ficheros de forma eficiente
"""


def count_of_matches_in_a_file(file_path, matches):
    """Cuenta el numero de coincidencias en un archivo dada la ruta del fichero y la función de coincidencia

    :param file_path: La ruta del fichero de texto a analizar
    :param matches: La función de coincidencia
    :return: El número de líneas en el que se cumple la condicion dad por la función matches
    """
    count = 0
    with open(file_path, "r") as file:
        for line in file:
            if matches(line):
                count = count + 1
    return count


