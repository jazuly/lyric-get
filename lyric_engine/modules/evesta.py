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
site_url = 'http://lyric.evesta.jp'
test_url = 'http://lyric.evesta.jp/l7bb423.html'

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
        prefix = '<div id="lyricbody">'
        suffix = '</div>'
        lyric = common.find_string_by_prefix_suffix(html, prefix, suffix, False)
        if not lyric:
            logging.info('Failed to parse lyric from html [%s]', html)
            return False

        lyric = lyric.replace('<br>', '\n')
        lyric = lyric.strip()
        lyric = common.unicode2string(lyric)
        lyric = common.half2full(lyric)

        self.lyric = lyric

        return True

    def parse_song_info(self, html):
        prefix = '<div id="lyrictitle">'
        suffix = '</div>'
        block = common.find_string_by_prefix_suffix(html, prefix, suffix, False)

        patterns = {
            'title': u'<h1>(.*?) 歌詞</h1>',
            'artist': u'>歌：(.*?)</p>',
            'lyricist': u'>作詞：(.*?)</p>',
            'composer': u'>作曲：(.*?)</p>'
        }

        for key in patterns:
            pattern = patterns[key]

            value = common.get_first_group_by_pattern(block, pattern)
            if value:
                value = common.strip_tags(common.htmlspecialchars_decode(value)).strip()
                setattr(self, key, value)
            else:
                logging.debug('Failed to get %s, pattern: %s' % (key, pattern, ))

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
