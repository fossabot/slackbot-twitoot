import os.path
import toml
from mastodon import Mastodon

CONFIG = toml.load(open('config.toml', encoding='utf-8'))


def toot_by_id(mastodon_id, toot_text, toot_media_list) -> (bool, dict):
    return toot(toot_text,
                toot_media_list,
                mastodon_id['server'],
                mastodon_id['client_key'],
                mastodon_id['client_secret'],
                mastodon_id['access_token'])


def toot(toot_text,
         toot_media_list,
         server_url,
         client_key,
         client_secret,
         access_token) -> (bool, dict):
    """
    tootを行うメソッド
    :param str toot_text: tootする内容
    :param list toot_media_list: tootに添付するメディアのパスのリスト
    :param str server_url: サーバURL e.g. https://mstdn.example.com
    :param str client_key: client_key
    :param str client_secret: client_secret
    :param str access_token: access_token
    :return: (bool, dict)で成否とresponse or errorを返す
    """

    # TODO: check inputs, imgリストは要チェック, とりあえず実装した...
    if toot_media_list:
        for media in toot_media_list:
            check_path = CONFIG['system']['path_tmp']+media
            is_valid = os.path.isfile(check_path)
            if not is_valid:
                return False, 'invalid media path:'+check_path

    # generate client_id.txt
    client_info_path = CONFIG['system']['path_tmp']+'client_id.txt'
    client_info = client_key + '\n' + client_secret
    f = open(client_info_path, 'w')
    f.write(client_info)
    f.close()

    try:
        mastodon = Mastodon(client_id=client_info_path, access_token=access_token, api_base_url=server_url)
        if toot_media_list is None:
            result = True, mastodon.toot(toot_text)
        else:
            # mediaをアップロードした結果をtootに添付すれば画像付きtootができる
            imgs = [mastodon.media_post(media) for media in toot_media_list]
            result = True, mastodon.status_post(status=toot_text, media_ids=imgs)
    except Exception as e:
        result = False, e
    finally:
        return result


if __name__ == '__main__':
    SECRET = toml.load(open('../secret.toml', encoding='utf-8'))
    mastodon1 = {"server": SECRET['mastodon']['server_1']['url'],
                 "client_key": SECRET['mastodon']['server_1']['app_1']['client_key'],
                 "client_secret": SECRET['mastodon']['server_1']['app_1']['client_secret'],
                 "access_token": SECRET['mastodon']['server_1']['app_1']['id_1']['access_token']}
    print(toot_by_id(mastodon1, 'a', None))  # TODO: ここで実行するとrootのパスが変わるからconfig.toml, cliend_id.txtが読めない、クラスにすればよさげ？


