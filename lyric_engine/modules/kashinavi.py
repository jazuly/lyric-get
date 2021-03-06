# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'KashiNavi'
site_index = 'kashinavi'
site_keyword = 'kashinavi'
site_url = 'http://kashinavi.com/'
test_url = 'http://kashinavi.com/song_view.html?65545'

class KashiNavi(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_html(url)
        if not html:
            logging.info('Failed to get html of url [%s]', url)
            return False

        if not self.find_lyric(url, html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(url, html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_html(self, url):
        resp = common.get_url_content(url)

        encoding = 'sjis'
        html = resp.decode(encoding, 'ignore')

        return html

    def find_lyric(self, url, html):
        prefix = '<p oncopy="return false;" unselectable="on;">'
        suffix = '</p>'

        lyric = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        lyric = lyric.replace('<br>', '\n')
        lyric = common.strip_tags(lyric)
        lyric = lyric.strip()

        self.lyric = lyric

        return True

    def find_song_info(self, url, html):
        ret = True

        prefix = '<table border=0 cellpadding=0 cellspacing=5>'
        suffix = '</td></table>'
        infoString = common.get_string_by_start_end_string(prefix, suffix, html)

        self.title = common.strip_tags(
            common.get_string_by_start_end_string('<td>', '</td>', infoString)
        )

        self.artist = common.strip_tags(
            common.get_string_by_start_end_string('<td><a href=', '</a></td>', infoString)
        )

        prefix = '<table border=0 cellpadding=0 cellspacing=0>'
        suffix = '</td></table>'
        lyricAndMusic = common.get_string_by_start_end_string(prefix, suffix, infoString)

        pattern = u'作詞　：　(.*)<br>'
        self.lyricist = common.get_first_group_by_pattern(lyricAndMusic, pattern)

        pattern = u'作曲　：　(.*)</td>'
        self.composer = common.get_first_group_by_pattern(lyricAndMusic, pattern)

        return ret

def get_lyric(url):
    obj = KashiNavi(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
