import json
import os
import re
import string
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from roundteam.config import load_yaml
import sys
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans


def cluster_users(data, clustering_algorithm, data_preprocessor):
    print('preprocessing data...')
    features = data_preprocessor.fit_transform(data)
    print('clustering...')
    clustering_algorithm.fit(features)


def get_text_cleaner(lang):
    # Sorting stop_words to remove long words first.
    # Otherwise in phrase I'm "I" can be removed first, leaving 'm behind
    stop_words = get_stop_words(lang)
    stop_words.extend(['rt', 'via', 'http', 'https', 'htt', 'ht']) # Sometimes twitter cut URL in the middle of URL
    stop_words = sorted(stop_words, reverse=True)

    translator = str.maketrans({key: None for key in string.punctuation})
    translator[ord(u"\u2026")] = None # Adding horizontal ellipsis as it's regularly included into Tweets
    del translator[ord('_')]

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    # import nltk
    # nltk.download()

    def clean_up_text(text):
        text = text.lower()

        # Removing URLs
        text = re.sub(r"https?:\/\/.*?(?:\r|\n|\s|$)", ' ', text, flags=re.MULTILINE)

        # Removing stop-words
        for stop_word in stop_words:
            pattern = r'\b' + stop_word.lower() + r'\b'
            text = re.sub(pattern, ' ', text, flags=re.MULTILINE)

        # Removing punctuation
        text = text.translate(translator)

        # Normalizing spaces
        text = re.sub(r"\s+", ' ', text.strip())

        # text = ' '.join(map(stemmer.stem, text.split(' ')))
        text = ' '.join(map(lemmatizer.lemmatize, text.split(' ')))

        return text
    return clean_up_text


def get_data(data_folder, max_users=-1):
    user_ids = []
    bags_of_words = []
    n_users = 0
    # TODO: Move to config?
    lang = 'en'
    clean_up_text = get_text_cleaner(lang)
    for filename in os.listdir(data_folder):
        if not filename.endswith('.json'):
            continue
        if max_users > 0 and n_users > max_users-1:
            break

        user_ids.append(filename[:-len('.json')])
        with open(os.path.abspath('%s/%s' % (data_folder, filename)), 'r') as f:
            tweets = json.load(f)
        tweet_texts = [tweet['full_text'] if 'full_text' in tweet else tweet['text'] for tweet in tweets if tweet['lang'] == lang]
        if len(tweet_texts) > 0:
            full_text = clean_up_text(' '.join(tweet_texts))
            bags_of_words.append(full_text)
        n_users += 1
    return bags_of_words


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


if __name__ == '__main__':
    dir = os.path.dirname(__file__)
    config = load_yaml(os.path.join(dir, '../config.yml'))
    max_users = config.clustering.max_users
    data_folder = config.tweets_folder
    if not os.path.isdir(data_folder):
        print('Data folder not found: %s' % data_folder)
        sys.exit(1)

    data = get_data(data_folder, config.clustering.max_users)
    tfidf = TfidfTransformer()
    cv = CountVectorizer(strip_accents='unicode')
    lda = LatentDirichletAllocation(n_topics=config.clustering.n_topics,
                                    verbose=1,
                                    learning_method='batch',
                                    topic_word_prior=config.clustering.gamma,
                                    max_iter=config.clustering.max_iterations)
    pipeline = Pipeline([
        ('vect', cv),
        ('tfidf', tfidf),
        ('clst', lda),
    ])
    pipeline.fit_transform(data)
    # cluster_users(data, lda, cv)
    print_top_words(lda, cv.get_feature_names(), 20)

