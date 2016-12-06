import json
import os
import re
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


if __name__ == '__main__':
    user_ids = []
    bags_of_words = []
    for filename in os.listdir('../data/tweets'):
        if not filename.endswith('.json'):
            continue
        user_ids.append(filename[:-len('.json')])
        with open('data/%s' % filename, 'r') as f:
            tweets = json.load(f)
        tweet_texts = [tweet['full_text'] if 'full_text' in tweet else tweet['text'] for tweet in tweets if tweet['lang'] == 'en']
        if len(tweet_texts) > 0:
            full_text = ' '.join(tweet_texts)
            full_text = re.sub(r'^RT\s', ' ', full_text, flags=re.MULTILINE | re.IGNORECASE)
            bags_of_words.append()

    print('calculating features...')
    cv = CountVectorizer(strip_accents='unicode', stop_words='english')
    features = cv.fit_transform(bags_of_words)
    #tfidf = TfidfTransformer()
    #features = tfidf.fit_transform(features)

    print('calculating lda...')
    lda = LatentDirichletAllocation(n_topics=30, verbose=1, learning_method='batch', topic_word_prior=0.02, max_iter=500)
    lda.fit(features)
    print_top_words(lda, cv.get_feature_names(), 10)



