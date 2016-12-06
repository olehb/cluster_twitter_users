import tweepy
import json

MAX_RECORDS = 1

consumer_key = 'wxwczZwiA3peVZZWq9qp3w'
consumer_secret = 'IfD3AvPwW2DsetwTupcmQPqU0rseqtM9YNPd3e2FNgM'
access_token = '22168865-9rIa3yIpBceZotEC4EIODh2a82fTiCqn3yow1ZoQs'
access_token_secret = 'zogWTsVjWlkwqD0hIIf63Pu5rlX9elfAC0mOGOpbeZj4o'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for i, user_id in enumerate(open('user_ids.csv', 'r')):
    user_id = user_id.strip()
    tweets = api.user_timeline(user_id=user_id)

    with open('data/%s.json' % user_id, 'w') as f:
        json.dump([tweet._json for tweet in tweets], f)

    if MAX_RECORDS > 0 and i > MAX_RECORDS-2:
        break
