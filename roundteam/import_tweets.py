import tweepy
import json
import time
from roundteam.config import load_yaml


def create_twitter_client(app_key, app_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(app_key, app_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def fetch_tweets(user_ids, twitter_client, dest_folder, tweets_per_user=100, max_users=-1, acceptable_failure_ratio=0.1):
    # TODO: Unit-test this
    n_failures = 0
    for i, user_id in enumerate(user_ids):
        if max_users > 0 and i > max_users-1:
            break
        try:
            tweets = twitter_client.user_timeline(user_id=user_id, count=tweets_per_user,
                                                  include_rts=True, tweet_mode='extended')
            with open('%s/%s.json' % (dest_folder, user_id), 'w') as f:
                json.dump([tweet._json for tweet in tweets], f)
            # This is needed to stay in Twitter API rate limit (900 in 15 minutes in this case).
            time.sleep(1)
        except tweepy.error.TweepError as ex:
            # TODO: Log these errors to file for further analysis, if needed.
            n_failures += 1

        if i > 0 and float(n_failures)/i > acceptable_failure_ratio:
            raise ValueError('too many failures: %d out of %d' % (n_failures, i))


if __name__ == '__main__':
    config = load_yaml('../config.yml')
    twitter_client = create_twitter_client(config.twitter.consumer_key, config.twitter.consumer_secret,
                                           config.twitter.access_token, config.twitter.access_token_secret)
    with open(config.user_ids_file) as f:
        user_ids = [user_id.strip() for user_id in f]

    fetch_tweets(user_ids, twitter_client, '.', 10, 2)
