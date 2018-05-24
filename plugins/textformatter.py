import re
import emoji


class TextFormatter(object):

    @staticmethod
    def format(text) -> str:
        """
        Slack RTM APIで受け取った文章を整形(以下の変更を加えて入力した文章に戻す)するための関数。
        1) emojiをtext形式(e.g., :innocent:)からunicodeにする。
        2) ウェブサイトのURLの前後につく括弧を削除する(e.g., '<https://ebiiim.com>' -> 'https://ebiiim.com')

        :param str text: 整形対象の文章
        :return: 整形後の文章
        """
        ret = TextFormatter._url_rm_brackets(text)
        ret = TextFormatter._str2emoji(ret)
        return ret

    @staticmethod
    def check(text) -> (bool, str):
        """
        フォーマットした後に問題が発生するかどうかをチェックする関数。
        (e.g., :upside_down_face:はformatで変換できない(emojizeで未対応))
        問題があった場合はFlaseと問題が発生した箇所をstrで返す。
        そうでない場合はTrueを返す。

        :param str text: チェック対象文章
        :return: (True/False, ''/問題の箇所)
        """
        return TextFormatter._is_safe_emoji(text)

    @staticmethod
    def _url_rm_brackets(text) -> str:
        # URLの外側に<>がある場合は削除する
        return re.sub(r'<(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)>', r'\1', text)

    @staticmethod
    def _str2emoji(text) -> str:
        return emoji.emojize(text, use_aliases=True)

    @staticmethod
    def _is_safe_emoji(text) -> (bool, str):
        f = TextFormatter.format(text)

        # emojizeした後にはtext形式のemoji(e.g., :innocent:)は存在しないと仮定
        # emojizeした後に:.+:があるなら(False, マッチしたパターン)を返す
        # emoji以外で:.+:にマッチするものがある場合は必ずエラーが出るので要注意
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
