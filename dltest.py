import shutil
import requests
import toml

CONFIG = toml.load(open('config.toml', encoding='utf-8'))

URL = CONFIG['test']['img_url']
save_path = './tmp/' + URL.split('/')[-1]

res = requests.get(URL, stream=True)
with open(save_path, "wb") as fp:
    shutil.copyfileobj(res.raw, fp)  # Windowsだとwgetが使えないので...
