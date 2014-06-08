# coding: utf-8
import os
import sys
module_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'modules')
sys.path.append(module_dir)

import unittest
from petitlyrics import PetitLyrics as Lyric

class PetitLyricsTest(unittest.TestCase):
    def test_url_01(self):
        url = 'http://petitlyrics.com/lyrics/34690'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'Tune The Rainbow')
        self.assertEqual(obj.artist, u'坂本 真綾')
        self.assertEqual(obj.lyricist, u'岩里 祐穂')
        self.assertEqual(obj.composer, u'菅野 よう子')
        self.assertEqual(len(obj.lyric), 819)

    def test_url_02(self):
        url = 'http://petitlyrics.com/lyrics/936622'
        obj = Lyric(url)
        obj.parse()

        self.assertEqual(obj.title, u'RPG')
        self.assertEqual(obj.artist, u'SEKAI NO OWARI')
        self.assertEqual(obj.lyricist, u'Saori/Fukase')
        self.assertEqual(obj.composer, u'Fukase')
        self.assertEqual(len(obj.lyric), 933)

if __name__ == '__main__':
    unittest.main()
