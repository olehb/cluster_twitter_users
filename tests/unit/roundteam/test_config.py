import unittest
from roundteam.config import Config


class ConfigTestCase(unittest.TestCase):
    def test_config(self):
        content = {
            'a': '111',
            'b': [1, 2, 3],
            'c': {
                'a': 123,
                'd': 'hello world'
            }
        }
        config = Config(content)
        self.assertEqual(config.a, '111')
        self.assertEqual(config.b, [1, 2, 3])
        self.assertIsInstance(config.c, Config)
        self.assertIsInstance(config.c.a, 123)
        self.assertRaises(config.something_else, ValueError)
        self.assertRaises(config.c.something_else, ValueError)


if __name__ == '__main__':
    unittest.main()
