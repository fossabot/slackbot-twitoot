from requests_oauthlib import OAuth1Session
import toml

SECRET = toml.load(open('secret.toml', encoding='utf-8'))
CONFIG = toml.load(open('config.toml', encoding='utf-8'))


def tweet(tweet_text,
          tweet_media_list,
          consumer_key=SECRET['twitter']['app_1']['consumer_key'],
          consumer_secret=SECRET['twitter']['app_1']['consumer_secret'],
          access_token=SECRET['twitter']['app_1']['id_1']['access_token'],
          access_token_secret=SECRET['twitter']['app_1']['id_1']['access_token_secret']) -> (bool, dict):

    twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

    if tweet_media_list:
        # media付きtweet
        pass
    else:
        try:
            params = {"status": tweet_text}
            return True, twitter.post(CONFIG['twitter']['url_text'], params=params)
        except Exception as e:
            return False, e

