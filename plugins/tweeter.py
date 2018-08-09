import os
import json
from requests_oauthlib import OAuth1Session
from logging import getLogger
logger = getLogger(__name__)


class Tweeter(object):

    URL_POST_MEDIA = 'https://upload.twitter.com/1.1/media/upload.json'
    URL_POST_TEXT = 'https://api.twitter.com/1.1/statuses/update.json'
    # TwitterのImageは5MB以下 {"errors":[{"code":324,"message":"Image file size must be <= 5242880 bytes"}]}
    MAX_IMAGE_SIZE = 5242880

    @staticmethod
    def tweet_by_id(twitter_id, tweet_text, media_list) -> (bool, dict):
        return Tweeter.tweet(tweet_text,
                             media_list,
                             twitter_id['consumer_key'],
                             twitter_id['consumer_secret'],
                             twitter_id['access_token'],
                             twitter_id['access_token_secret'])

    @staticmethod
    def tweet(tweet_text,
              media_list,
              consumer_key,
              consumer_secret,
              access_token,
              access_token_secret) -> (bool, dict):
        """
        tweetを行うメソッド
        :param tweet_text: 本文
        :param media_list: 添付するメディアのパスのリスト
        :param consumer_key: consumer_key
        :param consumer_secret: consumer_secret
        :param access_token: access_token
        :param access_token_secret: access_token_secret
        :return: (isSuccess, response)
        """
        if not media_list:
            media_list = []

        try:
            # validate media_list: invalidな要素があるならtweetしないでFalseを返す
            for medium in media_list:
                check_path = medium
                is_valid = os.path.isfile(check_path)
                if is_valid and os.path.getsize(check_path) > Tweeter.MAX_IMAGE_SIZE:
                    msg = 'too large: ' + check_path + ', the max size is ' + str(Tweeter.MAX_IMAGE_SIZE)
                    logger.error(msg)
                    return False, msg
                if not is_valid:
                    msg = 'invalid media path:' + check_path
                    logger.error(msg)
                    return False, msg
        except Exception as e:
            logger.error(str(e))
            return False, e

        try:
            # start twitter session
            twitter_client = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

            # upload media
            media_ids = []
            for medium in media_list:
                files = {"media": open(medium, 'rb')}
                req_upload = twitter_client.post(Tweeter.URL_POST_MEDIA, files=files)
                if req_upload.status_code != 200:
                    logger.error('upload failed')
                    return False, 'failed to upload:' + medium
                media_ids.append(json.loads(req_upload.text)['media_id'])

            # media_idsのフォーマット
            # '123,456': OK, 123 and 456
            # '[123, 456]': NG, 123 only
            # '[123,456]' or '123, 456': NG, parameter is invalid
            media_ids_str = str(media_ids).replace(' ', '').replace('[', '').replace(']', '')

            # post
            params = {"status": tweet_text, "media_ids": media_ids_str}
            result = twitter_client.post(Tweeter.URL_POST_TEXT, params=params)
            logger.info(result)
            return True, result
        except Exception as e:
            logger.error(str(e))
            return False, e


if __name__ == '__main__':
    import toml
    SECRET = toml.load(open('../secret.toml', encoding='utf-8'))
    id1 = {"consumer_key": SECRET['twitter']['app_1']['consumer_key'],
           "consumer_secret": SECRET['twitter']['app_1']['consumer_secret'],
           "access_token": SECRET['twitter']['app_1']['id_1']['access_token'],
           "access_token_secret": SECRET['twitter']['app_1']['id_1']['access_token_secret']}
    print(Tweeter.tweet_by_id(id1, 'test1', None))
    print(Tweeter.tweet_by_id(id1, 'test2', ['../test/test1.png']))
    print(Tweeter.tweet_by_id(id1, 'test3', ['../test/test1.png', '../test/test2.png']))
