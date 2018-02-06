from requests_oauthlib import OAuth1Session
import toml

SECRET = toml.load(open('secret.toml', encoding='utf-8'))
CONFIG = toml.load(open('config.toml', encoding='utf-8'))

for account in ['id_'+ str(i+1) for i in range(1)]:  # 複数アカウント対応
    CK = SECRET['twitter']['app_1']['consumer_key']
    CS = SECRET['twitter']['app_1']['consumer_secret']
    AT = SECRET['twitter']['app_1'][account]['access_token']
    AS = SECRET['twitter']['app_1'][account]['access_token_secret']

    twitter = OAuth1Session(CK, CS, AT, AS)

    params = {"status": "test"}
    twitter.post(CONFIG['twitter']['url_text'], params=params)
