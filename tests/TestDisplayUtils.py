import unittest
from unittest.mock import Mock

from PEC4 import DisplayUtils


class TestFileUtils(unittest.TestCase):
    def test(self):
        mock = Mock()
        DisplayUtils.plot_bar_chart(mock)

        mock.plot.bar.assert_called_once()


if __name__ == '__main__':
    unittest.main()


# python -m unittest discover -s tests
# coverage run -m unittest discover -s tests
# coverage html
