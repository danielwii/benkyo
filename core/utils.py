# -*- coding: utf-8 -*-


def phonetic_wrapper(kana, kanji, marking):
    parts = marking.split(';')

    if not kanji:
        wrapped = '<div class="phonetic-word">' \
                  '<div class="kana">%s</div>' % kana + \
                  '</div>'
    elif not marking:
        wrapped = '<div class="phonetic-word">' \
                  '<div class="kana">%s</div>' % kana + \
                  '<div class="kanji">%s</div>' % kanji + \
                  '</div>'
    else:
        wrapped = kanji
        for index, part in enumerate(parts):
            to_kanji, from_kana = part.split(':')

            replaced_by = extract_by_pos(kana, from_kana)
            html_snippet = '<div class="phonetic-word">' \
                           '<div class="kana">%s</div>' % replaced_by + \
                           '<div class="kanji">%s</div>' \
                           '</div>'
            wrapped = wrap_word2(wrapped, len(kanji), to_kanji, html_snippet)

    return wrapped


def extract_by_pos(words, pos):
    """

    :param words:
    :param pos:
        pos is start-end, like (start, end]
    :return:
    """
    if '-' in pos:
        start, end = pos.split('-')
        return words[int(start): int(end) + 1]
    else:
        return words[int(pos)]


def wrap_word2(need_wrapped, origin_length, pos, to):
    """

    :param need_wrapped:
    :param origin_length:
    :param pos:
        start-end
    :param to:
    :return:
    """
    if '-' in pos:
        start, end = pos.split('-')
        print(start, end)
        return wrap_word(need_wrapped, origin_length, int(start), int(end) - int(start), to)
    else:
        return wrap_word(need_wrapped, origin_length, int(pos), 1, to)


def wrap_word(need_wrapped, origin_length, start, length, to):
    """

    :param need_wrapped:
        需要处理的字符串
    :param origin_length:
        最原始字符串长度
    :param start:
        替换的起始位置，基于原始字符串
    :param length:
        需要替换的长度
    :param to:
        替换为的部分，可包括 ％s 引用被替换的部分
    :return:
    """
    length_fix = len(need_wrapped) - origin_length
    need_wrapped_list = list(need_wrapped)
    if '%s' in to:
        need_replace = need_wrapped_list[length_fix + start:length_fix + start + length]
        wrapped_chars = to % ''.join(need_replace)
    else:
        wrapped_chars = to

    before = ''.join(need_wrapped_list[0:length_fix + start])
    after = ''.join(need_wrapped_list[length_fix + start + length:])
    return before + wrapped_chars + after
