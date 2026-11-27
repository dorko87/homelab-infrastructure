import unittest
from check_writing import findings

class WritingTests(unittest.TestCase):
    def test_prose(self):
        self.assertEqual(list(findings("plain\nword \u2014 word\nword \u2013 word")), [2, 3])

    def test_code_and_quotes(self):
        self.assertEqual(list(findings("```\na \u2014 b\n```\n> a \u2013 b\n`a \u2014 b`")), [])

    def test_fence_length(self):
        self.assertEqual(list(findings("````\n```\na \u2014 b\n````\na \u2014 b")), [5])

    def test_url(self):
        self.assertEqual(list(findings("https://example.invalid/a\u2014b")), [])

if __name__ == "__main__":
    unittest.main()
