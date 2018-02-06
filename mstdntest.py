import toml
from mastodon import Mastodon

SECRET = toml.load(open('secret.toml', encoding='utf-8'))
CONFIG = toml.load(open('config.toml', encoding='utf-8'))

def toot(toot_text,
         toot_media_list
         ,server_url=SECRET['mastodon']['server_1']['url'],
         client_key=SECRET['mastodon']['server_1']['app_1']['client_key'],
         client_secret=SECRET['mastodon']['server_1']['app_1']['client_secret'],
         access_token=SECRET['mastodon']['server_1']['app_1']['id_1']['access_token']) -> (bool, dict):
    """

    :param str toot_text: tootする内容
    :param list toot_media_list: tootに添付するメディアのURLsのリスト
    :param str server_url: サーバURL e.g. https://mstdn.example.com
    :param str client_key: client_key
    :param str client_secret: client_secret
    :param str access_token: access_token
    :return: (bool, dict)で成否とresponse or errorを返す
    """
    # check inputs
        # urlの末尾の/を削除
    # generate client_id.txt
    client_info_path = CONFIG['system']['path_tmp']+'client_id.txt'
    client_info = client_key + '\n' + client_secret
    f = open(client_info_path, 'w')
    f.write(client_info)
    f.close()

    try:
        mastodon = Mastodon(client_id=client_info_path, access_token=access_token, api_base_url=server_url)
        result = True, mastodon.toot(toot_text)
        # mediaをアップロードした結果をtootに添付すれば画像付きtootができる
        # result = mastodon.media_post('./tmp/EXAMPLE.png')
        # imgs = [result]
        # mastodon.status_post(status='toot with an img from python', media_ids=imgs)
    except Exception as e:
        result = False, e
    finally:
        return result


if __name__ == '__main__':
    print(toot('test from python', None))

