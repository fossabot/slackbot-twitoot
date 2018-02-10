import toml
import urllib
import oauth2 as oauth

# 設定ファイル
CONFIG = toml.load(open('config.toml', encoding='utf-8'))
SECRET = toml.load(open('secret.toml', encoding='utf-8'))

# 認証したいAppのconsumer_keyとconsumer_secret
consumer_key = SECRET['twitter']['app_1']['consumer_key']
consumer_secret = SECRET['twitter']['app_1']['consumer_secret']

request_token_url = CONFIG['twitter']['url_oauth_request_token']
access_token_url = CONFIG['twitter']['url_oauth_access_token']
authenticate_url = CONFIG['twitter']['url_oauth_authenticate']

# コールバックURL, 本プログラムでは実際にアクセスするためアクセスできるページを指定すること
callback_url = CONFIG['twitter']['url_oauth_callback']


def twitter_oauth():
    c = oauth.Consumer(key=consumer_key, secret=consumer_secret)

    # get request token
    cl = oauth.Client(c)
    resp, content = cl.request(request_token_url + '?&oauth_callback=' + callback_url)
    request_token = dict(urllib.parse.parse_qs(content))[b'oauth_token'][0].decode('utf-8')
    # generate authorize_url
    authorize_url = authenticate_url + '?oauth_token=' + request_token

    print('\n\n\n\n\nTwitterのアプリ認証を行います。\n')
    print('1. Twitterにログインした状態で次のURLにアクセスし、「連携アプリを認証」ボタンを押して下さい。')
    print('URL:', authorize_url)
    print('\n2. すると、callback_urlに飛ばされるので、そのURLを丸ごとここに貼りつけて、Return/Enterを押してください。')
    print('(環境によっては、Return/Enterを押すとURLにアクセスしてしまう場合があります。該当する場合は後ろに半角スペースをつけてください。)')

    s = input('入力待ち > ')
    v = [value.split('=')[1] for value in s.strip().split('?')[1].split('&')]
    # get access token
    oauth_token = v[0]
    oauth_verifier = v[1]
    cl = oauth.Client(c, oauth.Token(oauth_token, oauth_verifier))
    resp, content = cl.request(CONFIG['twitter']['url_oauth_access_token'], 'POST', body='oauth_verifier=' + oauth_verifier)
    result = content.decode('utf-8').split('&')

    print('\n==================================================')
    print('access_token: ' + result[0].split('=')[1])
    print('access_token_secret: ' + result[1].split('=')[1])
    print('==================================================')


if __name__ == '__main__':
    twitter_oauth()  # 複数回実行しても結果は同じ(tokenがresetされるわけではない)
