# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'Evesta'
site_index = 'evesta'
site_keyword = 'evesta'
site_url = 'http://www.evesta.jp/lyric/'
test_url = 'http://www.evesta.jp/lyric/artists/a10019/lyrics/l65161.html'

class Evesta(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_html(url)
        if not html:
            logging.info('Failed to get html of url [%s]', url)
            return False

        if not self.parse_lyric(html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.parse_song_info(html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_html(self, url):
        html = common.get_url_content(url)
        if not html:
            return False

        html = html.decode('utf-8', 'ignore')

        return html

    def parse_lyric(self, html):
        html = html.replace('\r\n', '')
        prefix = "<div class='body'><p>"
        suffix = '</p>'
        lyric = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not lyric:
            logging.info('Failed to parse lyric from html [%s]', html)
            return False

        lyric = lyric.replace('<br />', '\n')
        lyric = lyric.strip()
        lyric = common.unicode2string(lyric)
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def parse_song_info(self, html):
        pattern = u'<title>(.+?) 歌詞 / .*</title>'
        self.title = common.get_first_group_by_pattern(html, pattern)

        pattern = u"<div class='artists'>歌：(.*)　作詞：(.*)　作曲：(.*)</div>"
        matches = common.get_matches_by_pattern(html, pattern)
        if not matches:
            return False

        self.artist = matches.group(1)
        self.lyricist = matches.group(2)
        self.composer = matches.group(3)

        return True

def get_lyric(url):
    obj = Evesta(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
