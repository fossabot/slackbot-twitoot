import re
import emoji


class TextFormatter(object):

    @staticmethod
    def format(text) -> str:
        ret = TextFormatter.url_rm_brackets(text)
        ret = TextFormatter.str2emoji(ret)
        return ret

    @staticmethod
    def url_rm_brackets(text) -> str:
        return re.sub(r'<(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)>', r'\1', text)

    @staticmethod
    def str2emoji(text) -> str:
        return emoji.emojize(text, use_aliases=True)


if __name__ == '__main__':
    s = 'abc:innocent:de:grinning: <https://ebiiim.com/> fghij<<>>'
    print(TextFormatter.format(s))
