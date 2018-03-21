import os
from mastodon import Mastodon


class Tooter(object):

    @staticmethod
    def toot_by_id(mastodon_id, toot_text, media_list) -> (bool, dict):
        return Tooter.toot(toot_text,
                           media_list,
                           mastodon_id['server'],
                           mastodon_id['client_key'],
                           mastodon_id['client_secret'],
                           mastodon_id['access_token'])

    @staticmethod
    def toot(toot_text,
             media_list,
             server_url,
             client_key,
             client_secret,
             access_token) -> (bool, dict):
        """
        tootを行うメソッド
        :param str toot_text: 本文
        :param list media_list: 添付するメディアのパスのリスト
        :param str server_url: サーバURL e.g. https://mstdn.example.com
        :param str client_key: client_key
        :param str client_secret: client_secret
        :param str access_token: access_token
        :return: (isSuccess, response)
        """

        if not media_list:
            media_list = []

        # validate media_list: invalidな要素があるならtootしないでFalseを返す
        try:
            for medium in media_list:
                check_path = medium
                is_valid = os.path.isfile(check_path)
                if not is_valid:
                    return False, 'invalid media path:' + check_path
        except Exception as e:
            return False, e

        # Mastodon()で必要なclient_idの一時ファイルを生成する
        client_info_path = 'tmp_client_id.txt'  # a tmp file
        with open(client_info_path, 'w') as f:
            # generate tmp_client_id.txt
            client_info = client_key + '\n' + client_secret
            f.write(client_info)
            f.close()

        try:
            # start mastodon session
            mastodon = Mastodon(client_id=client_info_path, access_token=access_token, api_base_url=server_url)
            # mediaをアップロードした結果をtootに添付すれば画像付きtootができる
            media_ids = [mastodon.media_post(media) for media in media_list]
            return True, mastodon.status_post(status=toot_text, media_ids=media_ids)
        except Exception as e:
            return False, e
        finally:
            # delete tmp_client_id.txt
            if os.path.isfile(client_info_path):
                os.remove(client_info_path)


if __name__ == '__main__':
    import toml
    SECRET = toml.load(open('../secret.toml', encoding='utf-8'))
    id1 = {"server": SECRET['mastodon']['server_1']['url'],
           "client_key": SECRET['mastodon']['server_1']['app_1']['client_key'],
           "client_secret": SECRET['mastodon']['server_1']['app_1']['client_secret'],
           "access_token": SECRET['mastodon']['server_1']['app_1']['id_1']['access_token']}
    print(Tooter.toot_by_id(id1, 'test1', None))
    print(Tooter.toot_by_id(id1, 'test2', ['../test/test1.png']))
    print(Tooter.toot_by_id(id1, 'test3', ['../test/test1.png', '../test/test2.png']))
