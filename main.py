import pandas as pd
import re

from PEC4 import DisplayUtils
from PEC4 import FileUtils
from PEC4 import DataframeOperations

pd.set_option('display.max_colwidth', None)

# Ejercicio 1. Apartados 1.1 y 1.2
#En el caso del 1.2, lo realizaria de la misma forma que en el 1.1

def is_huffington_post_in_line(line):
    # lambda line: "Huffington Post" in line
    return "Huffington Post" in line


def has_pdf_url(line):
    return re.search(r"https{0,1}.*?\.pdf", line)


count_huffington = FileUtils.count_of_matches_in_a_file("PEC4/resources/covid_approval_polls.csv", is_huffington_post_in_line)
count_urls = FileUtils.count_of_matches_in_a_file("PEC4/resources/covid_approval_polls.csv", has_pdf_url)

print("El numero de veces que se repite Huffington Post es", count_huffington)
print("El numero de veces que se encontró la url con pdf es", count_urls)

# 1.3
# Crearía un threadpool con las 100 tareas creando 5 o 10 (dependiendo de la velocidad de lectura del HDD o SDD) para aprovechar la CPU y la lectura de disco tanto como sea posible.
# Hay que tener cuidado de no crear demasiados hilos, pues esto supondría un cuello de botella en la lectura de disco.


# Ejercicio 2
# Voy a usar Pandas porque nos premite leer de una forma sencilla y rápida csv y xlsx creando dataframes que están optimizados por la librearia

approval_polls = pd.read_csv("PEC4/resources/covid_approval_polls.csv", sep=",")
concern_polls = pd.read_csv("PEC4/resources/covid_concern_polls.csv", sep=",")
pollster_rating = pd.read_excel("PEC4/resources/pollster_ratings.xlsx")

approval_polls = DataframeOperations.filter_interviews_by_tracking_and_pollster(approval_polls, pollster_rating)
concern_polls = DataframeOperations.filter_interviews_by_tracking_and_pollster(concern_polls, pollster_rating)

# Ejercicio 3

ejer3df = DataframeOperations.get_approve_analysis_by_party(approval_polls)
DisplayUtils.plot_bar_chart(ejer3df)


# Ejercicio 4
# 4.1

print(DataframeOperations.number_of_people_per_interview(concern_polls))

# 4.2
df42 = DataframeOperations.concerned_people_number(concern_polls, "economy")
DisplayUtils.plot_bar_chart(df42)

# 4.3
df43 = DataframeOperations.concerned_people_percentage(concern_polls, "infected")
DisplayUtils.plot_bar_chart(df43)

# 4.4
df44_temp = DataframeOperations.normalise_grades(pollster_rating)
df44_temp2 = concern_polls[["end_date", "pollster", "text", "very", "somewhat", "not_very", "not_at_all", "sample_size"]]
df44 = DataframeOperations.merge_two_dataframes(df44_temp2, df44_temp, "pollster", "Pollster", True)
df44_grouped = DataframeOperations.group_interviews_by_grade(df44)
DisplayUtils.plot_bar_chart(df44_grouped)

# 5
df5 = DataframeOperations.set_mark_based_on_grade_and_predictive_plus_minus(df44)

# 5.1
df51 = df5[df5["mark"] >= 1.5] #  Filter by mark

# 5.1a
df51a = DataframeOperations.ejer51a(df51)
DisplayUtils.plot_bar_chart(DataframeOperations.ejer51a_grouped(df51a))

# 5.1b
df51b = DataframeOperations.ejer51b(df51a)
DisplayUtils.plot_bar_chart(df51b)

# 5.2 Los datos mostrados en porcentaje son mucho más representativos. Debido a la gran diferencia de entrevistas entre los
# dos grupos de fechas, era muy difícil de visualizar los datos en la primera gráfica.

