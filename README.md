# slackbot-twitoot
SlackからTwitterとMastodonに同時投稿するためのbotです。

**使い方**
> `@bot_name ttt つぶやきたい内容`

botをチャンネルに追加して↑のようなメンションを送ります。画像を付ける場合はUpload時のコメント欄に書きます。

## 概要
あの青い鳥の夜逃げに備えて、自分のつぶやきを象さんにバックアップしたいというピンポイントすぎる用途に最適です。

Python3で動きます。つぶやきたい内容をSlackに書くと、[RTM API](https://api.slack.com/rtm)でそれを受信して、TwitterとMastodonに流します。とても単純です。~~なのにスパゲティコード🍝~~

## 導入方法
三種の神器ならぬ三種のアクセストークンが必要です。

**cloneしてrequirementsをインストール**
```
git clone https://github.com/ebiiim/slackbot-twitoot && cd slackbot-twitoot
pip3 install -r requirements.txt
```

**secret.tomlにトークン等を入力** [(詳細)](#secret.toml)
```
cp secret.toml.sample secret.toml
vi secret.toml
```

**実行**
```
python3 run.py
```

- [OpenCVの関連でエラーが出る場合](#opencv)

## 更新履歴
- 2018-02-03 `hello, world`
- 2018-02-10 v0.1.0 とりあえずつぶやけます
- 2018-03-25 v0.2.0 画像付きでつぶやけます
- 2018-04-01 v0.2.1 ↑ウソでした(エイプリルフールではありません)

## TODO
- 機能
    - 絵文字に対応する
    - 画像が複数枚ある場合にも対応する
    - ログ関連をイイ感じにする

- 既知のバグ
    - たまにRTMのコネクションが切れて落ちる...

## 細かいこと

### <a name="secret.toml"> secret.toml
```
[slack]
oauth_token = ''
bot_token = ''
```
Slack Appを作成し、アクセストークンを入力します。
1. [https://api.slack.com/apps](https://api.slack.com/apps) -> `Create New App`
1. 左側メニュー`Bot Users` -> `Add a Bot User`
1. 左側メニュー`OAuth & Permissions` -> `Scopes` -> `files:read`と`files:write:user`を追加
1. 左側メニュー`Basic Information` -> `Install your app to your workspace` からAppをインストール
1. 左側メニュー`OAuth & Permissions`の`OAuth Access Token`を`oauth_token`に、`Bot User OAuth Access Token`を`bot_token`に入力

```
[twitter]
    [twitter.app_1]
    consumer_key = ''
    consumer_secret = ''
        [twitter.app_1.id_1]
        access_token = ''
        access_token_secret = ''
```
Twitterに投稿するために利用します。
- [https://apps.twitter.com](https://apps.twitter.com) から`Create New App`すると全部埋まります。

```
[mastodon]
    [mastodon.server_1]
    url = ''
        [mastodon.server_1.app_1]
        client_key = ''
        client_secret = ''
            [mastodon.server_1.app_1.id_1]
            access_token = ''
```
Mastodonに投稿するために利用します。
- `url`には利用するサーバのURLを入力してください。(e.g. `https://mstdn.jp`)
- ブラウザからMastodonにログインし、設定画面の`開発`から`新規アプリ`を作成すると残りが埋まります。

### <a name="opencv"> OpenCVのimportに失敗する場合
```
sudo apt install -y libsm6 libxrender1
```
