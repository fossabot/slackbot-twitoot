import time
from slackclient import SlackClient
import logging
import toml

# 設定ファイル
CONFIG = toml.load(open('config.toml', encoding='utf-8'))
SECRET = toml.load(open('secret.toml', encoding='utf-8'))

# 認証後に代入する
bot_id = None

# a handler which displays logs to console
logging.getLogger().setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logging.getLogger().addHandler(ch)

sc = SlackClient(SECRET['slack']['api_token'])


def handle_cmd_kill(cmd):
    cmds = cmd.split()
    if len(cmds) > 1:
        if cmds[1] in ['you', 'お前']:
            return CONFIG['bot']['res_kill_you']
    return CONFIG['bot']['res_kill']


def handle_command(cmd, channel):
    response = CONFIG['bot']['res_default']

    if cmd.startswith(('help', '-h', '--help', '使い方', 'a')):
        response = CONFIG['bot']['res_help']
    elif cmd.startswith('kill'):
        response = handle_cmd_kill(cmd)

    sc.api_call('chat.postMessage', channel=channel, text=response, as_user=True)


def parse_slack_cmd(cmd):
    at_bot = '<@' + bot_id + '>'
    for elem in cmd:
        logging.debug("Parsing: " + str(cmd))
        if ('text' in elem) and (at_bot in elem['text']):
            return elem['text'].split(at_bot)[1], elem['channel']
    return None, None


if __name__ == '__main__':
    RTM_READ_DELAY = CONFIG['common']['rtm_interval']
    if sc.rtm_connect():
        logging.info('Bot connected and running!')
        # Read bot's user ID by calling Web API method <auth.test>
        bot_id = sc.api_call("auth.test")["user_id"]
        while True:
            cmd, channel = parse_slack_cmd(sc.rtm_read())
            if cmd and channel:
                handle_command(cmd, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        logging.warning('Connection failed.')
