import unicodedata
import re


def normalize_string(text: str, replace_spaces: str = " "):
    try:
        text = unicode(text, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")\
        .lower()

    sub_texts = []

    try:
        for sub in text.split(" "):
            sub_texts.append(re.sub('[^A-Za-z0-9]+', '', sub))
    except Exception as e:
        pass

    return replace_spaces.join(sub_texts)


if __name__ == "__main__":
    print(normalize_string("Héùlàïo iM'ka +=$*-éàççàu(çà!§-", "-"))
