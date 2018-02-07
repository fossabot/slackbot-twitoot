from requests_oauthlib import OAuth1Session
import toml

CONFIG = toml.load(open('config.toml', encoding='utf-8'))


def tweet_by_id(twitter_id, tweet_text, tweet_media_list) -> (bool, dict):
    return tweet(tweet_text,
                 tweet_media_list,
                 twitter_id['consumer_key'],
                 twitter_id['consumer_secret'],
                 twitter_id['access_token'],
                 twitter_id['access_token_secret'])


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
            return True, twitter.post(CONFIG['twitter']['url_text'], params=params)
        except Exception as e:
            return False, e


if __name__ == '__main__':
    SECRET = toml.load(open('../secret.toml', encoding='utf-8'))
    twitter1 = {"consumer_key": SECRET['twitter']['app_1']['consumer_key'],
                "consumer_secret": SECRET['twitter']['app_1']['consumer_secret'],
                "access_token": SECRET['twitter']['app_1']['id_1']['access_token'],
                "access_token_secret": SECRET['twitter']['app_1']['id_1']['access_token_secret']}
    print(tweet_by_id(twitter1, 'a', None))  # TODO: ここで実行するとrootのパスが変わるからconfig.tomlが読めない、クラスにすればよさげ？

