#!/usr/bin/env python3

from urllib import request as req
from urllib.parse import urlparse as uparse
import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
download_dir = 'events/'
download_path = os.path.join(root_dir, download_dir)

'''
empties the events-folder to guarantee the latest state of the calendar.
Yes i know this is dirty and I should not simply redownload the wohle calendar
'''
def cleanup():
    for f in os.listdir(download_path):
        f_path = os.path.join(download_path, f)
        if os.path.isfile(f_path):
            os.remove(f_path)

'''
download all events for a given calendar
@params:
    url: URL of the ics-file to download
    username: caldav-user
    password: corresponding passwod
'''
def dl(url, username, password):
    if not url:
        return 1

    file_name = url.split('/')[-1]
    file_path = os.path.join(download_path, file_name)

    base_url = uparse(url).scheme + "://" + uparse(url).netloc

    pwmg = req.HTTPPasswordMgrWithDefaultRealm()
    pwmg.add_password(None, base_url, username, password)

    handler = req.HTTPBasicAuthHandler(pwmg)

    opener = req.build_opener(handler)
    opener.open(url)
    req.install_opener(opener)


    u = req.urlopen(url)
    f = open(file_path, 'wb')

    file_size_dl = 0
    block_sz = 8192
    while True:
        buf = u.read(block_sz)
        if not buf:
            break

        file_size_dl += len(buf)
        f.write(buf)
    f.close()
