import re
import emoji


class TextFormatter(object):

    @staticmethod
    def format(text) -> str:
        ret = TextFormatter.url_rm_brackets(text)
        ret = TextFormatter.str2emoji(ret)
        return ret

    @staticmethod
    def check(text) -> (bool, str):
        return TextFormatter.is_safe_emoji(text)

    @staticmethod
    def url_rm_brackets(text) -> str:
        return re.sub(r'<(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)>', r'\1', text)

    @staticmethod
    def str2emoji(text) -> str:
        return emoji.emojize(text, use_aliases=True)

    @staticmethod
    def is_safe_emoji(text) -> (bool, str):

        f = TextFormatter.format(text)

        pattern = r":.+:"
        match_obj = re.search(pattern, f)

        if match_obj:
            return False, match_obj.group()

        return True, ''


if __name__ == '__main__':
    s = 'abc:innocent:de:grinning: <https://ebiiim.com/> fghij<<>>'
    print(TextFormatter.format(s))
    print(TextFormatter.check(s))
    s = ':innocent::sleeping::zzz::blush::package::upside_down_face:'
    print(TextFormatter.format(s))
    print(TextFormatter.check(s))

