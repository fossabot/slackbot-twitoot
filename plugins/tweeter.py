from requests_oauthlib import OAuth1Session


class Tweeter(object):

    post_media_url = 'https://upload.twitter.com/1.1/media/upload.json'
    post_text_url = 'https://api.twitter.com/1.1/statuses/update.json'

    @staticmethod
    def tweet_by_id(twitter_id, tweet_text, tweet_media_list) -> (bool, dict):
        return Tweeter.tweet(tweet_text,
                             tweet_media_list,
                             twitter_id['consumer_key'],
                             twitter_id['consumer_secret'],
                             twitter_id['access_token'],
                             twitter_id['access_token_secret'])

    @staticmethod
    def tweet(tweet_text,
              tweet_media_list,
              consumer_key,
              consumer_secret,
              access_token,
              access_token_secret) -> (bool, dict):
        twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
        if tweet_media_list:
            # media付きtweet
            pass
        else:
            try:
                params = {"status": tweet_text}
                return True, twitter.post(Tweeter.post_text_url, params=params)
            except Exception as e:
                return False, e


if __name__ == '__main__':
    import toml
    SECRET = toml.load(open('../secret.toml', encoding='utf-8'))
    id2 = {"consumer_key": SECRET['twitter']['app_1']['consumer_key'],
           "consumer_secret": SECRET['twitter']['app_1']['consumer_secret'],
           "access_token": SECRET['twitter']['app_1']['id_2']['access_token'],
           "access_token_secret": SECRET['twitter']['app_1']['id_2']['access_token_secret']}
    print(Tweeter.tweet_by_id(id2, 'abc', None))
