import shutil
import requests
import time
from slackclient import SlackClient
import logging
import toml
import plugins.tooter as tooter
import plugins.tweeter as tweeter

# 設定ファイル
CONFIG = toml.load(open('config.toml', encoding='utf-8'))
SECRET = toml.load(open('secret.toml', encoding='utf-8'))

# 認証後に代入する
bot_id = None

# ログの設定(ログはコンソールに表示する)
logging.getLogger().setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logging.getLogger().addHandler(ch)

sc = SlackClient(SECRET['slack']['api_token'])


def handle_cmd_sns(cmd, img_path):

    # TODO: 構造が汚い！
    mastodon1 = {"server": SECRET['mastodon']['server_1']['url'],
                 "client_key": SECRET['mastodon']['server_1']['app_1']['client_key'],
                 "client_secret": SECRET['mastodon']['server_1']['app_1']['client_secret'],
                 "access_token": SECRET['mastodon']['server_1']['app_1']['id_1']['access_token']}

    twitter1 = {"consumer_key": SECRET['twitter']['app_1']['consumer_key'],
                "consumer_secret": SECRET['twitter']['app_1']['consumer_secret'],
                "access_token": SECRET['twitter']['app_1']['id_1']['access_token'],
                "access_token_secret": SECRET['twitter']['app_1']['id_1']['access_token_secret']}

    logging.info('Handling cmd SNS: ' + cmd + ',' + str(img_path))
    return tweet(twitter1, cmd, img_path) + '\n' + toot(mastodon1, cmd, img_path)

def tweet(twitter_id, text, img_path):
    # イメージ1個のみを想定
    logging.info('Tweeting: ' + cmd + ',' + str(img_path))
    is_success, result = tweeter.tweet_by_id(twitter_id, text, img_path)
    return CONFIG['bot']['res_tweet'] + ':' + str(is_success)  # + ', ' + str(result)


def toot(mastodon_id, text, img_path):
    # イメージ1個のみを想定
    logging.info('Tooting: ' + cmd + ',' + str(img_path))
    is_success, result = tooter.toot_by_id(mastodon_id, text, img_path)
    return CONFIG['bot']['res_toot'] + ':' + str(is_success)  # + ', ' + str(result)


def download_img(url):
    # TODO: デフォルトのブラウザでSlackにログインしている状態でのみ確認しています...

    # jpeg -> jpg Mastodon対応してないと思ってたけどそんなことなかった...これいらないのでは？
    exe = url.split('/')[-1].split('.')[-1]
    if exe == 'jpeg':
        exe = 'jpg'
    filename = ''.join(url.split('/')[-1].split('.')[:-1]) + '.' + exe

    save_path = CONFIG['system']['path_tmp'] + filename
    res = requests.get(url, stream=True)
    with open(save_path, "wb") as fp:
        shutil.copyfileobj(res.raw, fp)
    return save_path


def handle_cmd_kill(cmd):
    """
    killコマンドの処理を行うメソッド
    :param cmd: botにメンションで送ったメッセージ
    :return: Slackに投稿するメッセージ
    """
    cmds = cmd.split()
    if len(cmds) > 1:
        if cmds[1] in ['you', 'お前']:
            return CONFIG['bot']['res_kill_you']
    return CONFIG['bot']['res_kill']


def handle_command_with_img(cmd, channel, img_url):
    logging.info('Handling img cmd: ' + img_url + ',' + cmd)
    img_path = download_img(img_url)
    logging.info('File saved: ' + img_url + '->' + img_path)

    response = CONFIG['bot']['res_img_default']

    if cmd.startswith(CONFIG['bot']['cmd_sns']):
        response = handle_cmd_sns(cmd[len(CONFIG['bot']['cmd_sns'])+1:], img_url)  # cmdの"しゃべる "以降のみ
    return sc.api_call('chat.postMessage', channel=channel, text=response, as_user=True)


def handle_command(cmd, channel):
    """
    botに対するメンションを処理するメソッド, file_url=Noneの場合のコマンドの識別および処理の実施を行う
    :param cmd: コマンド(botに対するメンション)
    :param channel: Slackの対象チャンネル
    :return: サーバの応答(Slackの対象チャンネルにコマンドの実行結果を投稿した結果)
    """
    response = CONFIG['bot']['res_default']
    logging.info('Handling cmd: ' + cmd)
    if cmd.startswith(('help', '-h', '--help', '使い方', 'a')):
        response = CONFIG['bot']['res_help']
    elif cmd.startswith('kill'):
        response = handle_cmd_kill(cmd)
    elif cmd.startswith(CONFIG['bot']['cmd_sns']):  # cmdの"しゃべる "以降のみ
        response = handle_cmd_sns(cmd[len(CONFIG['bot']['cmd_sns'])+1:], None)  # 画像無しSNS投稿

    return sc.api_call('chat.postMessage', channel=channel, text=response, as_user=True)


def parse_slack_cmd(cmd):
    """
    RTM(Real Time Messaging) APIで受け取ったメッセージをパースするメソッド, botに対するメンションのみを認識する
    :param cmd: RTMで受け取ったJSON
    :return: (botに対するメンション, 対象チャンネル, 画像ファイルのURL)
    """
    at_bot = '<@' + bot_id + '>'
    for elem in cmd:
        logging.debug("Parsing: " + str(cmd))
        if ('text' in elem) and (at_bot in elem['text']):  # cmd[text]の中を見て、botに対するメンションの場合のみ
            if len(elem['text'].split('uploaded a file: <')) > 1:  # ファイルアップロード
                if elem['text'].split('uploaded a file: <')[1].split('|')[0].split('.')[-1] in ['png','jpg','jpeg', 'bmp', 'gif']:  # Slackは拡張子をlowercaseで保存する
                    logging.info("Parsing: mention img txt")
                    file_url = elem['text'].split('uploaded a file: <')[1].split('|')[0]
                    return elem['text'].split(at_bot)[1].strip(), elem['channel'], file_url
            else:
                logging.info("Parsing: mention txt")
                return elem['text'].split(at_bot)[1].strip(), elem['channel'], None
    return None, None, None


if __name__ == '__main__':
    RTM_READ_DELAY = CONFIG['system']['rtm_interval']
    if sc.rtm_connect():
        logging.info('Bot connected and running!')
        bot_id = sc.api_call("auth.test")["user_id"]  # botのuser IDを取得する
        while True:  # コマンド待ち
            cmd, channel, file_url = parse_slack_cmd(sc.rtm_read())
            if cmd and channel and not file_url:  # 画像なしメンション
                logging.info('Handled: mention txt  -> ' + str(handle_command(cmd, channel)))
            elif cmd and channel and file_url:  # 画像付きメンション
                logging.info('Handled: mention img txt  -> ' + str(handle_command_with_img(cmd, channel, file_url)))
            time.sleep(RTM_READ_DELAY)
    else:
        logging.warning('Connection failed.')
