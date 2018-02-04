import toml
from mastodon import Mastodon

SECRET = toml.load(open('secret.toml', encoding='utf-8'))
CONFIG = toml.load(open('config.toml', encoding='utf-8'))

server_url = SECRET['mastodon']['server_1']['url']

client_info = SECRET['mastodon']['server_1']['app_1']['client_key'] + '\n' + SECRET['mastodon']['server_1']['app_1']['client_secret']
client_info_path = CONFIG['system']['path_tmp']+'client_id.txt'

access_token = SECRET['mastodon']['server_1']['app_1']['id_1']['access_token']

f = open(client_info_path, 'w')
f.write(client_info)
f.close()

mastodon = Mastodon(client_id=client_info_path, access_token=access_token, api_base_url=server_url)
mastodon.toot('test from python')
