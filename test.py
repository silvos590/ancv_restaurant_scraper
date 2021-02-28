import unittest
from unittest.mock import patch 
from io import StringIO
import ancv_html_scraper as ancv

class TestHelp(unittest.TestCase):
    def test_help(self):
        """
        Test that the helper works
        """
        with patch('sys.stdout', new = StringIO()) as fake_out:
            ancv.usage()
            self.assertTrue(fake_out.getvalue().startswith("Usage: "))

if __name__ == '__main__':
    unittest.main()