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
        self.assertEqual(config.c.a, 123)
        with self.assertRaises(ValueError):
            config.something_else
        with self.assertRaises(ValueError):
            config.c.something_else


if __name__ == '__main__':
    unittest.main()
