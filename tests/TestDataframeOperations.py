import unittest

import pandas as pd
from PEC4 import DataframeOperations


class TestDataframeOperations(unittest.TestCase):
    def test_merge_two_dataframes_deleting_column(self):
        df1 = pd.DataFrame.from_dict({'col_1': [1, 2], 'col_2': ['a', 'b']})
        df2 = pd.DataFrame.from_dict({'col_3': [1, 2], 'col_4': ['A', 'B']})

        result = DataframeOperations.merge_two_dataframes(df1, df2, "col_1", "col_3", True)

        self.assertIn("col_4", list(result.columns), "Deberia contener la col_4 ")
        self.assertNotIn("col_3", list(result.columns), "Deberia contener la col_3 ")
        self.assertEqual([1, "a", "A"], list(result.iloc[0]), "Deberia ser [1, \"a\", \"A\"]")
        self.assertEqual(2, result.shape[0], "Tendra 2 filas")
        self.assertEqual(3, result.shape[1], "Tendra 3 columnas")
        pass

    def test_merge_two_dataframes_without_deleting_column(self):
        df1 = pd.DataFrame.from_dict({'col_1': [1, 2], 'col_2': ['a', 'b']})
        df2 = pd.DataFrame.from_dict({'col_3': [1, 2], 'col_4': ['A', 'B']})

        result = DataframeOperations.merge_two_dataframes(df1, df2, "col_1", "col_3", False)

        self.assertIn("col_4", list(result.columns), "Deberia contener la col_4 ")
        self.assertIn("col_3", list(result.columns), "Deberia contener la col_3")
        self.assertEqual([1, "a", 1, "A"], list(result.iloc[0]), "Deberia ser [1, \"a\", 1, \"A\"]")
        self.assertEqual(2, result.shape[0], "Tendra 2 filas")
        self.assertEqual(4, result.shape[1], "Tendra 3 columnas")
        pass

    def test_filter_interviews_by_tracking_and_pollster(self):
        polls = pd.DataFrame.from_dict({'pollster': ["Juan", "Manolo", "Juan"], 'tracking': [True, False, False],
                                        'text': ['interview1', 'interview2', 'interview3']})
        pollsters = pd.DataFrame.from_dict({'Pollster': ["Pepito", "Juan"], "Banned by 538": ["yes", "no"]})

        result = DataframeOperations.filter_interviews_by_tracking_and_pollster(polls, pollsters)

        self.assertEqual(1, result.shape[0], "Tendra una fila")

    def test_get_approve_analysis_by_party(self):
        polls = pd.DataFrame.from_dict(
            {'text': ["coronavirus y luego Trump", "Trump y luego coronavirus", "Solo Trump"],
             'approve': [50, 100, 23],
             'sample_size': [100, 200, 23],
             'disapprove': [50, 0, 23],
             'party': ['P.A', "P.A", "P.B"]
             })

        result = DataframeOperations.get_approve_analysis_by_party(polls)

        self.assertEqual(1, result.shape[0], "Tendra una fila")
        self.assertEqual(250, result.iloc[0]["n_approve"], "Tendra 250 filas")
        self.assertEqual(50, result.iloc[0]["n_disapprove"], "Tendra 50 filas")

    def test_number_of_people_per_interview(self):
        polls = pd.DataFrame.from_dict({'text': ["interview1", "interview1", "interview2"],
                                        'sample_size': [100, 200, 23]
                                        })

        result = DataframeOperations.number_of_people_per_interview(polls)

        self.assertEqual(2, result.shape[0], "Tendra 2 filas")
        self.assertEqual(300, result[result.index == "interview1"].values[0], "Seran 300")
        self.assertEqual(23, result[result.index == "interview2"].values[0], "Seran 23")

    def test_concerned_people_number(self):
        polls = pd.DataFrame.from_dict(
            {'subject': ["concern-economy", "concern-economy", "concern-religion"],
             'very': [50, 75, 23],
             'sample_size': [100, 200, 23],
             'not_at_all': [25, 10, 0]
             })

        result = DataframeOperations.concerned_people_number(polls, "economy")

        self.assertEqual(1, result.shape[0], "Sera una fila")
        self.assertEqual(1, len(result[result.index == "concern-economy"]), "Solo 1 resultado")
        self.assertEqual(200, result[result.index == "concern-economy"].values[0][0], "200 resultados")
        self.assertEqual(45, result[result.index == "concern-economy"].values[0][1], "45 resultados")
        self.assertEqual(0, len(result[result.index == "concern-religion"]), "No deberia devolver nada")

    def test_concerned_people_number(self):
        polls = pd.DataFrame.from_dict(
            {'subject': ["concern-economy", "concern-economy", "concern-religion"],
             'very': [50, 50, 23],
             'sample_size': [100, 200, 23],
             'not_at_all': [10, 30, 0]
             })

        result = DataframeOperations.concerned_people_percentage(polls, "economy")

        self.assertEqual(1, result.shape[0], "Should have exactly 1 row")
        self.assertEqual(1, len(result[result.index == "concern-economy"]), "Solo 1 resultado")
        self.assertEqual(50, result[result.index == "concern-economy"].values[0][0], "Seria el 50%")
        self.assertEqual(20, result[result.index == "concern-economy"].values[0][1], "Seria el  45%")
        self.assertEqual(0, len(result[result.index == "concern-religion"]), "No deberia devolver nada")

    def test_normalise_grades(self):
        pollsters = pd.DataFrame.from_dict({'Pollster': ["Pepito", "Juanito", "Josete", "Antoñito"],
                                            "538 Grade": ["A+", "B-", "C/D", "F"]})

        result = DataframeOperations.normalise_grades(pollsters)

        self.assertEqual("A", result[result["Pollster"] == "Pepito"]["538 Grade"].iloc[0], "Sera A cuando es Pepito")
        self.assertEqual("B", result[result["Pollster"] == "Juanito"]["538 Grade"].iloc[0], "Sera B cuando es Juanito")
        self.assertEqual("D", result[result["Pollster"] == "Josete"]["538 Grade"].iloc[0], "Sera D cuando es Josete")
        self.assertEqual("F", result[result["Pollster"] == "Antoñito"]["538 Grade"].iloc[0], "Sera F cuando sea Antoñito")

    def test_group_interviews_by_grade(self):
        polls = pd.DataFrame.from_dict({'text': ["interview1", "interview2", "interview3", "interview4"],
                                            "538 Grade": ["A", "B", "A", "D"]})

        result = DataframeOperations.group_interviews_by_grade(polls)

        self.assertEqual(2, result[result.index == "A"].values[0], "Sera 2")
        self.assertEqual(1, result[result.index == "B"].values[0], "Sera  1")
        self.assertEqual(1, result[result.index == "D"].values[0], "Sera  1")

    def test_set_mark_based_on_grade_and_predictive_plus_minus(self):
        polls = pd.DataFrame.from_dict({'Pollster': ["1", "2", "3", "4", "5"],
                                        "538 Grade": ["A", "B", "C", "D", "F"],
                                        "Predictive    Plus-Minus": [1, 1, 1, 1, 1]
                                        })

        result = DataframeOperations.set_mark_based_on_grade_and_predictive_plus_minus(polls)

        self.assertEqual(2, result[result["Pollster"] == "1"]["mark"].iloc[0], "Sera  2")
        self.assertEqual(1.5, result[result["Pollster"] == "2"]["mark"].iloc[0], "Sera  1.5")
        self.assertEqual(1, result[result["Pollster"] == "3"]["mark"].iloc[0], "Sera  1")
        self.assertEqual(0.5, result[result["Pollster"] == "4"]["mark"].iloc[0], "Sera  0.5")
        self.assertEqual(0, result[result["Pollster"] == "5"]["mark"].iloc[0], "Sera  0")

    def test_set_mark_based_on_grade_and_predictive_plus_minus_invalid_grade(self):
        polls = pd.DataFrame.from_dict({'Pollster': ["1"],
                                        "538 Grade": ["E"],
                                        "Predictive    Plus-Minus": [1]
                                        })

        with self.assertRaises(Exception):
            DataframeOperations.set_mark_based_on_grade_and_predictive_plus_minus(polls)

    def test_ejer51a(self):
        polls = pd.DataFrame.from_dict({'end_date': ["2020-09-01", "2020-09-01", "2019-01-01"],
                                        "very": [10, 10, 10],
                                        "somewhat": [50, 10, 50],
                                        "not_very": [30, 30, 50],
                                        "not_at_all": [40, 40, 50],
                                        "sample_size": [100, 1000, 200]
                                        })

        result = DataframeOperations.ejer51a(polls)

        self.assertEqual(3, result.shape[0], "Should have exactly 3 rows")
        self.assertEqual("After 2020-09-01", result.iloc[0]["date_group"], "Contendra el grupo After 2020-09-01 ")
        self.assertEqual("After 2020-09-01", result.iloc[1]["date_group"], "Contendra el grupo 2020-09-01")
        self.assertEqual("Before 2020-09-01", result.iloc[2]["date_group"], "Contendra el grupo 2020-09-01 ")
        self.assertEqual(10, result.iloc[0]["n_very"], "Sera 10")
        self.assertEqual(50, result.iloc[0]["n_somewhat"], "Sera   50")
        self.assertEqual(30, result.iloc[0]["n_not_very"], "Sera   30")
        self.assertEqual(40, result.iloc[0]["n_not_at_all"], "Sera   40")

    def test_ejer51a_grouped(self):
        polls = pd.DataFrame.from_dict({'date_group': ["After 2020-09-01", "After 2020-09-01", "Before 2020-09-01", "Before 2020-09-01"],
                                        "text": ["interview1", "interview1", "interview2", "interview3"],
                                        "n_very": [10, 10, 10, 10],
                                        "n_somewhat": [50, 10, 50, 50],
                                        "n_not_very": [30, 30, 50, 50],
                                        "n_not_at_all": [40, 40, 50, 50]
                                        })

        result = DataframeOperations.ejer51a_grouped(polls)
        group1 = result[result.index == ("interview1", "After 2020-09-01")]
        group2 = result[result.index == ("interview2", "Before 2020-09-01")]

        self.assertEqual(3, result.shape[0], "Tendra 3 columnas")
        self.assertEqual(20, group1["n_very"].iloc[0], "Sera 20")
        self.assertEqual(60, group1["n_somewhat"].iloc[0], "Sera 60")
        self.assertEqual(60, group1["n_not_very"].iloc[0], "Sera 60")
        self.assertEqual(80, group1["n_not_at_all"].iloc[0], "Sera 80")

        self.assertEqual(10, group2["n_very"].iloc[0], "Sera 20")
        self.assertEqual(50, group2["n_somewhat"].iloc[0], "Sera 50")
        self.assertEqual(50, group2["n_not_very"].iloc[0], "Sera 50")
        self.assertEqual(50, group2["n_not_at_all"].iloc[0], "Sera 0")

    def test_ejer51b(self):
        polls = pd.DataFrame.from_dict({'date_group': ["After 2020-09-01", "After 2020-09-01", "Before 2020-09-01", "Before 2020-09-01"],
                                        "text": ["interview1", "interview1", "interview2", "interview3"],
                                        "n_very": [10, 10, 10, 20],
                                        "n_somewhat": [50, 10, 50, 60],
                                        "n_not_very": [30, 30, 20, 10],
                                        "n_not_at_all": [10, 50, 20, 10]
                                        })

        result = DataframeOperations.ejer51b(polls)
        group1 = result[result.index == ("interview1", "After 2020-09-01")]
        group2 = result[result.index == ("interview2", "Before 2020-09-01")]

        self.assertEqual(3, result.shape[0], "Should have exactly 3 rows")
        self.assertEqual(10, group1["per_very"].iloc[0], "Sera 10")
        self.assertEqual(30, group1["per_somewhat"].iloc[0], "Sera 30")
        self.assertEqual(30, group1["per_not_very"].iloc[0], "Sera 30")
        self.assertEqual(30, group1["per_not_at_all"].iloc[0], "Sera 30")

        self.assertEqual(10, group2["per_very"].iloc[0], "Sera 20")
        self.assertEqual(50, group2["per_somewhat"].iloc[0], "Sera 50")
        self.assertEqual(20, group2["per_not_very"].iloc[0], "Sera 20")
        self.assertEqual(20, group2["per_not_at_all"].iloc[0], "Sera 20")


if __name__ == '__main__':
    unittest.main()


# python -m unittest discover -s tests
# coverage report -m unittest discover -s tests
