# coding: utf-8
import os
import sys
include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'include')
sys.path.append(include_dir)

import json
import logging
import common
from lyric_base import LyricBase

site_class = 'JoySound'
site_index = 'joysound'
site_keyword = 'joysound'
site_url = 'http://joysound.com/'
test_url = 'https://www.joysound.com/web/search/song/26613'

class JoySound(LyricBase):
    def parse_page(self):
        url = self.url

        song_id = self.get_song_id(url)
        if not song_id:
            logging.info('Failed to song id from [%s]', url)
            return False

        logging.debug('Song ID is %s', song_id)

        json_obj = self.get_song_json(song_id)
        if not json_obj:
            logging.info('Failed to get song JSON of url [%s]', url)
            return False

        if not self.parse_lyric(json_obj):
            logging.info('Failed to get lyric of url [%s]', url)
            return False

        if not self.parse_song_info(json_obj):
            logging.info('Failed to get song info of url [%s]', url)

        return True

    def get_song_id(self, url):
        pattern = '/song/([0-9]+)'
        song_id = common.get_first_group_by_pattern(url, pattern)

        return song_id

    def get_song_json(self, song_id):
        json_url = 'https://mspxy.joysound.com/Common/Lyric'
        post_data = 'kind=naviGroupId&selSongNo=%s&interactionFlg=0&apiVer=1.0' % (song_id, )
        headers = {
            'X-JSP-APP-NAME': '0000800'
        }

        json_str = common.get_url_content(json_url, post_data, headers)

        if not json_str:
            logging.info('Failed to get json from url [%s]', url)
            return False

        obj = json.loads(json_str)

        return obj

    def parse_lyric(self, json_obj):
        if 'lyricList' not in json_obj:
            logging.info('No "lyricList" in song JSON')
            return False

        lyricList = json_obj['lyricList']
        if len(lyricList) < 1:
            logging.info('"lyricList" length < 1')
            return False

        value = lyricList[0]['lyric']
        value = value.strip()

        self.lyric = value

        return True

    def parse_song_info(self, json_obj):
        patterns = {
            'title': 'songName',
            'artist': 'artistName',
            'lyricist': 'lyricist',
            'composer': 'composer',
        }

        for key in patterns:
            json_key = patterns[key]

            if json_key in json_obj:
                value = json_obj[json_key]

                if value:
                    setattr(self, key, value)
        return True

def get_lyric(url):
    obj = JoySound(url)

    return obj.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    url = test_url

    full = get_lyric(url)
    if not full:
        print('Cannot get lyric')
        exit()
    print(full.encode('utf-8', 'ignore'))

