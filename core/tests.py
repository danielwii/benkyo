from django.test import TestCase

from core.mem_curve import calc_ranks
from core.utils import phonetic_wrapper, wrap_word, extract_by_pos


class TestCalc_ranks(TestCase):
    def test_calc_ranks(self):
        self.assertEqual((0, 0), calc_ranks(0, 0, True))
        # self.assertEqual((0, -5), calc_ranks(0, 1, True))
        self.assertEqual((2, 40), calc_ranks(0, 2, True))
        # self.assertEqual((0, 5), calc_ranks(0, 3, True))
        self.assertEqual((4, 60), calc_ranks(0, 4, True))

        # self.assertEqual((0, 0), calc_ranks(0, 0, False))
        self.assertEqual((2, 35), calc_ranks(40, 1, False))
        self.assertEqual((2, 40), calc_ranks(40, 2, False))
        self.assertEqual((3, 45), calc_ranks(40, 3, False))
        # self.assertEqual((3, 50), calc_ranks(0, 4, False))


# -*- coding: utf-8 -*-
class TestPhonetic_wrapper(TestCase):
    def test_phonetic_wrapper(self):
        self.assertEqual(phonetic_wrapper('ちゅうごくじん', '中国人', '0:0-2;1:3-4;2:4-5'), '<div class="phonetic-word"><div class="kana">ちゅう</div><div class="kanji">中</div></div><div class="phonetic-word"><div class="kana">ごく</div><div class="kanji">国</div></div><div class="phonetic-word"><div class="kana">くじ</div><div class="kanji">人</div></div>')

    def test_wrap_word(self):
        self.assertEqual(wrap_word('12345', 5, 2, 1, '<%s>'), '12<3>45')
        self.assertEqual(wrap_word('12345', 5, 2, 2, '<%s>'), '12<34>5')
        self.assertEqual(wrap_word('<1>2345', 5, 2, 2, '<%s>'), '<1>2<34>5')

    def test_extract(self):
        self.assertEqual(extract_by_pos('12345', '2'), '3')
        self.assertEqual(extract_by_pos('12345', '2-3'), '34')
