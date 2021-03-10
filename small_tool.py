#! -*- coding:utf-8 -*-
import os
import requests


def which(pgm):
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p

def download_img_url(url,folder):
    response = requests.get(url)
    file_name = url.split('/').pop()
    with open(folder+file_name+'.png', 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    print(which("adb"))
