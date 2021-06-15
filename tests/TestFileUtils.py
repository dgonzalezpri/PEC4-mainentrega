import unittest
import os
from PEC4 import FileUtils


DIR = os.path.dirname(os.path.realpath(__file__))


class TestFileUtils(unittest.TestCase):
    def test_count_of_matches_of_unittest_words_in_a_file(self):
        def unittest_in_line(line):
            return "unittest" in line

        counter = FileUtils.count_of_matches_in_a_file(DIR + "/resources/file.txt", unittest_in_line)
        self.assertEqual(counter, 1, "Should be 1")

    def test_count_of_matches_of_no_existing_word_in_a_file(self):
        def coverage_in_line(line):
            return "coverage" in line

        counter = FileUtils.count_of_matches_in_a_file(DIR + "/resources/file.txt", coverage_in_line)
        self.assertEqual(counter, 0, "Should be 0")


if __name__ == '__main__':
    unittest.main()
