import time
from slackclient import SlackClient
import logging
import toml

# 設定ファイル
CONFIG = toml.load(open('config.toml', encoding='utf-8'))
SECRET = toml.load(open('secret.toml', encoding='utf-8'))

# 認証後に代入する
bot_id = None

# ログの設定(ログはコンソールに表示する)
logging.getLogger().setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logging.getLogger().addHandler(ch)

sc = SlackClient(SECRET['slack']['api_token'])


def handle_cmd_sns(cmd):
    return tweet(cmd) + ',' + toot(cmd)


def tweet(cmd):
    logging.info('Tweet:'+cmd)
    return CONFIG['bot']['res_tweet']


def toot(cmd):
    logging.info('Toot:' + cmd)
    return CONFIG['bot']['res_toot']


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


def handle_command_with_file(cmd, channel, file_url):
    print('file upload detected!!!')


def handle_command(cmd, channel):
    """
    botに対するメンションを処理するメソッド, file_url=Noneの場合のコマンドの識別および処理の実施を行う
    :param cmd: コマンド(botに対するメンション)
    :param channel: Slackの対象チャンネル
    :return: サーバの応答(Slackの対象チャンネルにコマンドの実行結果を投稿した結果)
    """
    response = CONFIG['bot']['res_default']
    print(cmd)
    if cmd.startswith(('help', '-h', '--help', '使い方', 'a')):
        response = CONFIG['bot']['res_help']
    elif cmd.startswith('kill'):
        response = handle_cmd_kill(cmd)
    elif cmd.startswith(CONFIG['bot']['cmd_sns']):
        response = handle_cmd_sns(cmd)

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
                if elem['text'].split('uploaded a file: <')[1].split('|')[0].split('.')[-1].lower() in ['png','jpg','jpeg', 'bmp', 'gif']:
                    file_url = elem['text'].split('uploaded a file: <')[1].split('|')[0]
                    return elem['text'].split(at_bot)[1].strip(), elem['channel'], file_url
            else:
                return elem['text'].split(at_bot)[1].strip(), elem['channel'], None
    return None, None, None


if __name__ == '__main__':
    RTM_READ_DELAY = CONFIG['common']['rtm_interval']
    if sc.rtm_connect():
        logging.info('Bot connected and running!')
        bot_id = sc.api_call("auth.test")["user_id"]  # botのuser IDを取得する
        while True:  # コマンド待ち
            cmd, channel, file_url = parse_slack_cmd(sc.rtm_read())
            if cmd and channel and not file_url:  # 画像なしメンション
                logging.info(str(handle_command(cmd, channel)))
            elif cmd and channel and file_url:  # 画像付きメンション
                logging.info(str(handle_command_with_file(cmd, channel, file_url)))
            time.sleep(RTM_READ_DELAY)
    else:
        logging.warning('Connection failed.')
