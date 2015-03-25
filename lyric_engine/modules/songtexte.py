# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import logging
import common
from lyric_base import LyricBase

site_class = 'SongTexte'
site_index = 'songtexte'
site_keyword = 'songtexte'
site_url = 'http://www.songtexte.com/'
test_url = 'http://www.songtexte.com/songtext/taylor-swift/begin-again-63a6de47.html'

class SongTexte(LyricBase):
    def parse_page(self):
        url = self.url

        html = self.get_lyric_html(url)
        if not html:
            logging.info('Failed to get lyric html of url [%s]', url)
            return False

        if not self.find_lyric(html):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.find_song_info(html):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_lyric_html(self, url):
        raw = common.get_url_content(url)

        html = raw.decode('utf-8', 'ignore')

        return html

    def find_lyric(self, html):
        prefix = '<div id="lyrics">'
        suffix = '</div>'
        rawLyric = common.get_string_by_start_end_string(prefix, suffix, html)

        rawLyric = rawLyric.replace('<br/>', '\n')
        rawLyric = common.unicode2string(rawLyric)
        rawLyric = common.strip_tags(rawLyric).strip()

        self.lyric = rawLyric

        return True

    def sanitize(self, src):
        return common.unicode2string(common.htmlspecialchars_decode(src))

    def find_song_info(self, html):
        ret = True

        pattern = 'og:title" content="(.*) - (.*) Songtext"'

        regex = common.get_matches_by_pattern(html, pattern)
        if regex:
            self.artist = self.sanitize(regex.group(1))
            self.title = self.sanitize(regex.group(2))

        return ret

def get_lyric(url):
    obj = SongTexte(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    url = 'http://www.songtexte.com/songtext/bone-thugs-n-harmony-feat-mariah-carey-and-bow-wow/c-town-6ba75a7e.html'

    full = get_lyric(url)
    if not full:
        print('Failed to get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))
