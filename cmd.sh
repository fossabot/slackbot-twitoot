#!/bin/sh

sed -i -e "/self.fh = logging.FileHandler(log_file_name, mode='a', encoding=None, delay=False)/d" run.py
sed -i -e "/self.fh.setLevel(log_level_file)/d" run.py
sed -i -e "/self.fh.setFormatter(self.formatter)/d" run.py
sed -i -e "/logging.getLogger().addHandler(self.fh)/d" run.py

sed -i -e "s/oauth_token = ''/oauth_token = '$OAUTH_TOKEN'/" secret.toml
sed -i -e "s/bot_token = ''/bot_token = '$BOT_TOKEN'/" secret.toml
sed -i -e "s/consumer_key = ''/consumer_key = '$TWITTER_CONSUMER_KEY'/" secret.toml
sed -i -e "s/consumer_secret = ''/consumer_secret = '$TWITTER_CONSUMER_SECRET'/" secret.toml
sed -i -e "1s/access_token = ''/access_token = '$TWITTER_ACCESS_TOKEN'/" secret.toml
sed -i -e "s/access_token_secret = ''/access_token_secret = '$TWITTER_ACCESS_TOKEN_SECRET'/" secret.toml
sed -i -e "s#url = ''#url = '$MASTODON_URL'#" secret.toml
sed -i -e "s/client_key = ''/client_key = '$MASTODON_CLIENT_KEY'/" secret.toml
sed -i -e "s/client_secret = ''/client_secret = '$MASTODON_CLIENT_SECRET'/" secret.toml
sed -i -e "s/access_token = ''/access_token = '$MASTODON_ACCESS_TOKEN'/" secret.toml

python3 run.py

