#!python3
# -*- coding:UTF-8 -*-
import requests,json,time,sys
from contextlib import closing

class get_photos(object):
    def __init__(self):
        self.photos_id = []
        self.download_server = 'https://unsplash.com/photos/xxx/download?force=trues'
        self.target = 'http://unsplash.com/napi/feeds/home'
        self.headers = {'authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}
    
    def get_ids(self):
        req = requests.get(url=self.target, headers=self.headers,verify=False)
        html = json.loads(req.text)
        next_page = html['next_page']
        for each in html['photos']:
            self.photos_id.append(each['id'])
        time.sleep(1)
        for i in range(4):
            req = requests.get(url=next_page, headers=self.headers,verify=False)
            html = json.loads(req.text)
            next_page = html['next_page']
            for each in html['photos']:
                self.photos_id.append(each['id'])
            time.sleep(1)

    def download(self, photo_id, filename):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        target = self.download_server.replace('xxx', photo_id)
        with closing(requests.get(url = target, stream = True, verify= False, headers = self.headers)) as r:
            with open('%d.jpg' % filename,'ab+') as f:
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

if __name__ == '__main__':
    gp = get_photos()
    print('get photos links:')
    gp.get_ids()
    print('downloading photos:')
    for i in range(len(gp.photos_id)):
        print('download %d photos'%(i+1))
        gp.download(gp.photos_id[i],(i+1))
