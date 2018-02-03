from requests_oauthlib import OAuth1Session
import toml

SECRET = toml.load(open('secret.toml', encoding='utf-8'))
CONFIG = toml.load(open('config.toml', encoding='utf-8'))

for account in ['twitter-ebiiiiim']:  # 複数アカウント対応
    CK = SECRET[account]['consumer_key']
    CS = SECRET[account]['consumer_secret']
    AT = SECRET[account]['access_token']
    AS = SECRET[account]['access_token_secret']

    twitter = OAuth1Session(CK, CS, AT, AS)

    params = {"status": "test"}
    twitter.post(CONFIG['twitter']['url_text'], params=params)
