import json
import os
import re
import config
import sys
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


def clean_up_text(text):
    text = text.lower()
    stop_words = get_stop_words('en')
    stop_words.append('rt')
    for stop_word in stop_words:
        pattern = r'\b' + stop_word.lower() + r'\b'
        text = re.sub(pattern, ' ', text, flags=re.MULTILINE)
    text = re.sub(r'https?:\/\/.*[\r\n\s$]', ' ', text, flags=re.MULTILINE | re.IGNORECASE)
    return text


def cluster_users(data_folder, max_users=-1):
    user_ids = []
    bags_of_words = []
    n_users = 0
    for filename in os.listdir(data_folder):
        if not filename.endswith('.json'):
            continue
        if max_users > 0 and n_users > max_users-1:
            break

        user_ids.append(filename[:-len('.json')])
        with open(os.path.abspath('%s/%s' % (data_folder, filename)), 'r') as f:
            tweets = json.load(f)
        tweet_texts = [tweet['full_text'] if 'full_text' in tweet else tweet['text'] for tweet in tweets if tweet['lang'] == 'en']
        if len(tweet_texts) > 0:
            full_text = clean_up_text(' '.join(tweet_texts))
            bags_of_words.append(full_text)
        n_users += 1

    print('loaded data for %d users' % n_users)
    print('calculating features...')
    cv = CountVectorizer(strip_accents='unicode')
    features = cv.fit_transform(bags_of_words)
    #tfidf = TfidfTransformer()
    #features = tfidf.fit_transform(features)

    print('calculating lda...')
    lda = LatentDirichletAllocation(n_topics=30, verbose=1, learning_method='batch', topic_word_prior=0.02, max_iter=500)
    lda.fit(features)
    print_top_words(lda, cv.get_feature_names(), 10)


if __name__ == '__main__':
    config = config.load_yaml('../../config.yml')
    max_users = config.clustering.max_users
    data_folder = config.tweets_folder
    if not os.path.isdir(data_folder):
        print('Data folder not found: %s' % data_folder)
        sys.exit(1)
    cluster_users(data_folder, max_users)

