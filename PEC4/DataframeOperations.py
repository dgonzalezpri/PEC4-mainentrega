"""" Utilidad que provee de diferentes funcionalidades para trabajar con dataframes
"""
import pandas as pd


def merge_two_dataframes(df1, df2, df1_key, df2_key, delete_df2_key=False):
    """Dados dos dataframes los intersecta y devuelve el dataframe resultado de la operacion

    :param df1: primer dataframe a unir
    :param df2: segundo dataframe a unir
    :param df1_key: nombre de la columna del primer dataframe por la que queremos unir los dataframes
    :param df2_key: nombre de la columna del segundo dataframe por la que queremos unir los dataframes
    :param delete_df2_key: Indica si deseamos borrar la columna df2_key del dataframe final
    :return: la intersección de los dos dataframes pasados como parametros
    """
    tmp = pd.merge(df1, df2, left_on=df1_key, right_on=df2_key)
    if delete_df2_key:
        tmp = tmp.drop(df2_key, axis=1)
    return tmp


def filter_interviews_by_tracking_and_pollster(polls, pollster_rating):
    """ Filtra las entrevistas que tienen tracking, que sus entrevistadores no están en el pollster_rating y que sus
    entrevistadores han sido baneados

    :param polls: el dataframe de entrevistas a filtrar
    :param pollster_rating: el listado de entrevistadores
    :return: el dataframe de entrevistas filtrado
    """
    tmp = polls[polls["pollster"].isin(pollster_rating["Pollster"])]
    tmp = tmp[tmp["tracking"] == False]
    tmp = merge_two_dataframes(tmp, pollster_rating[["Pollster", "Banned by 538"]], 'pollster', 'Pollster', True)
    tmp = tmp[tmp["Banned by 538"] == "no"].drop("Banned by 538", axis=1)

    return tmp


def get_approve_analysis_by_party(polls):
    """ Dado un dataframe de entrevistas obtiene el número de entrevistados que aprueban o desaprueban las medidas
     agrupado por partido

    :param polls: El dataframe de aprobación/desaprobación con las entrevistas
    :return: El dataframe con el número de personas que aprueban y desaprueban las medidas agrupado por partido político
    """
    tmp = polls[polls["text"].str.contains(r"(?=.*\bTrump\b)(?=.*\bcoronavirus\b)")]
    tmp["n_approve"] = tmp["approve"] / 100 * tmp["sample_size"]
    tmp["n_disapprove"] = tmp["disapprove"] / 100 * tmp["sample_size"]
    tmp = tmp[["party", "n_approve", "n_disapprove"]]
    tmp = tmp.groupby(["party"])[["n_approve", "n_disapprove"]].sum()
    return tmp


def number_of_people_per_interview(concern_polls):
    """ Dado un dataframes de entrevistas devuelve un dataframe con el número de personas por entrevistas

    :param concern_polls: El dataframe de entrevistas
    :return: El dataframe con el número de personas por entrevistas
    """
    return concern_polls.groupby("text")["sample_size"].sum()


def concerned_people_number(polls, subject):
    """ Dado el dataframe de entrevistas devuelve otro dataframe con el número de personas (dedicadas a un sector)
    muy preocupadas y nada preocupadas

    :param polls: El dataframe de entrevistas
    :param subject: El sector de los entrevistados
    :return: El dataframe con el número de personas (dedicadas a un sector) muy preocupadas y nada preocupadas
    """
    df = polls
    df["n_very"] = df["very"] / 100 * df["sample_size"]
    df["n_not_at_all"] = df["not_at_all"] / 100 * df["sample_size"]
    df = df[df["subject"] == "concern-" + subject].groupby("subject")[["n_very", "n_not_at_all"]].sum()
    return df


def concerned_people_percentage(polls, subject):
    """Dado el dataframe de entrevistas devuelve otro dataframe con el porcentaje de personas (dedicadas a un sector)
    muy preocupadas y nada preocupadas

    :param polls: El dataframe de entrevistas
    :param subject: El sector de los entrevistados
    :return: El dataframe con el porcentaje de personas (dedicadas a un sector) muy preocupadas y nada preocupadas
    """
    df = polls
    df = df[df["subject"] == "concern-" + subject].groupby("subject")[["very", "not_at_all"]].mean()
    return df


def normalise_grades(pollster_rating):
    """ Dado un dataframe de entrevistadores normaliza los grados de los entrevistadores

    Ejemplos:
        B/C → C
        B- → B
        B+ → B

    :param pollster_rating: El dataframe de entrevistadores
    :return: El dataframe resultado de la intersección de los dataframes pasados como parametros normalizando el grado del entrevistador
    """

    def normalise(grade):
        grade = grade.split("/")[-1]  # Gets bigger grade
        grade = grade[0]  # Obtains only the letter
        return grade

    pollster_rating["538 Grade"] = pollster_rating["538 Grade"].apply(normalise)
    return pollster_rating


def group_interviews_by_grade(polls):
    """ Dado un dataframe de entrevistas intersectadas con su entrevistador agrupa las entrevistas por grado

    :param polls: Un dataframe de entrevistas intersectadas con su entrevistador
    :return: Un dataframe con las entrevistas agrupadas por grado
    """
    return polls.groupby("538 Grade")["text"].count()


def set_mark_based_on_grade_and_predictive_plus_minus(polls):
    """ Dado un dataframe de entrevistas calcula la nota evaluada (mark) en funcion de el grado y predictive plus-minus
    del entrevistador

    :param polls: Un dataframe de entrevistas intersectado con su entrevistador
    :return: El dataframe de entrada con la columna mark que contiene la nota evaluada de cada entrevista/entrevistador
    """
    df5 = polls

    grades_marks = {
        "A": 1,
        "B": 0.5,
        "C": 0,
        "D": -0.5,
        "F": -1,
    }

    def set_mark(row):
        row["mark"] = grades_marks[row["538 Grade"]] + row["Predictive    Plus-Minus"]
        return row

    df5 = df5.apply(set_mark, axis=1)  # Set mark
    return df5


def ejer51a(polls):
    """ Dado un dataframe calcula el número de personas según el nivel de preocupación (concern very, somewhat,...)
    y categoriza las entrevistas por aquellas realizadas estrictamente antes del 2020-09-01, o después

    :param polls: Un dataframe de entrevistas intersectado con su entrevistador
    :return: El dataframe de entrada con las columnas `n_very`, `n_somewhat`, `n_not_very`, `n_not_at_all` y `date_group`
    """
    def set_date_group(row):
        row["date_group"] = "Before 2020-09-01" if row["end_date"] < "2020-09-01" else "After 2020-09-01"
        return row

    df51a = polls.apply(set_date_group, axis=1)  # Generate date_group column

    df51a["n_very"] = df51a["very"] / 100 * df51a["sample_size"]
    df51a["n_somewhat"] = df51a["somewhat"] / 100 * df51a["sample_size"]
    df51a["n_not_very"] = df51a["not_very"] / 100 * df51a["sample_size"]
    df51a["n_not_at_all"] = df51a["not_at_all"] / 100 * df51a["sample_size"]
    return df51a


def ejer51a_grouped(polls):
    """ Dado un dataframe categorizado por antes del 2020-09-01 o después, agrupa por entrevista y grupo de fecha y
    suma el número de personas según su nivel de preocupación

    :param polls: Un dataframe categorizado por antes del 2020-09-01 o después
    :return: El dataframe de entrada con agrupado por entrevista y grupo de fecha
    """
    return polls.groupby(["text", "date_group"])[["n_very", "n_somewhat", "n_not_very", "n_not_at_all"]].sum()


def ejer51b(polls):
    """ Dado un dataframe categorizado por antes del 2020-09-01 o después, agrupa por entrevista y grupo de fecha y
        suma el porcentaje de personas según su nivel de preocupación

        :param polls: Un dataframe categorizado por antes del 2020-09-01 o después
        :return: El dataframe de entrada con agrupado por entrevista y grupo de fecha
        """
    def get_percent(row):
        total = row["n_very"] + row["n_somewhat"] + row["n_not_very"] + row["n_not_at_all"]
        row["per_very"] = (row["n_very"] / total) * 100
        row["per_somewhat"] = (row["n_somewhat"] / total) * 100
        row["per_not_very"] = (row["n_not_very"] / total) * 100
        row["per_not_at_all"] = (row["n_not_at_all"] / total) * 100
        return row

    df51b = polls.apply(get_percent, axis=1).groupby(["text", "date_group"])[
        ["per_very", "per_somewhat", "per_not_very", "per_not_at_all"]].mean()

    return df51b
