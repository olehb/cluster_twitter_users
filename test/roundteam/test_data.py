import unittest
from stop_words import get_stop_words
from random import shuffle

from roundteam.cluster_users import get_text_cleaner


class TestData(unittest.TestCase):
    def test_data_cleanup(self):
        clean_up_text = get_text_cleaner('en')

        text = "https://t.co/wekjh23 marsian agriculture"
        self.assertEqual('marsian agriculture', clean_up_text(text))

        # Note the space in the end
        text = "https://t.co/wekjh23 some_text http://sub.domain.example.com/ https://t.co/blahblha "
        self.assertEqual('some_text', clean_up_text(text))

        # No space in the end
        text = "https://t.co/wekjh23 some_text http://sub.domain.example.com/ https://t.co/blahblha "
        self.assertEqual('some_text', clean_up_text(text))

        text = "https://t.co/wekjh23"
        self.assertEqual('', clean_up_text(text))

        text = "https://t.co/wekjh23 hello."
        self.assertEqual('hello', clean_up_text(text))

        text = "HTTPS://T.CO/WEKJH23"
        self.assertEqual('', clean_up_text(text))

        text = "HTTPS://example.COM/blahablallala, and for and RT this_is_something_useful"
        self.assertEqual('this_is_something_useful', clean_up_text(text))

        text = "RT AND for and I'm are aren't did didn't"
        self.assertEqual('', clean_up_text(text))

        text = "RT   , , . ,. ,. , . ,.: ? !!!!!!!!! ;-) :)(        insanity FOR"
        self.assertEqual('insanity', clean_up_text(text))

        text = (u"\u2026" + " ")*10 + 'ellipsis was removed'
        self.assertEqual('ellipsis removed', clean_up_text(text))

        text = "https:…"
        self.assertEqual('', clean_up_text(text))

        text = "https:/…"
        self.assertEqual('', clean_up_text(text))

        stop_words = get_stop_words("en")
        for i in range(10):
            shuffle(stop_words)
            self.assertEqual('', clean_up_text(' '.join(stop_words)))


