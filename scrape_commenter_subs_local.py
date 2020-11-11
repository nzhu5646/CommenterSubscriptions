import re
import sys
import time
import os
import random
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pyvirtualdisplay import Display



def parse_subs(html):
    sub_l = []
    for chan_seg in html.split('<div id="channel" class="style-scope ytd-grid-channel-renderer">')[1:]:
        m = re.search('href="/channel/([^\"]+)">', chan_seg)
        if m is None: continue
        chan_id = m.group(1)
        m = re.search('<span id="title" class="style-scope ytd-grid-channel-renderer">([^\<]+)</span>', chan_seg)
        chan_name = m.group(1) if m is not None else ""
        m = re.search('<span id="thumbnail-attribution" class="style-scope ytd-grid-channel-renderer">(.+) subscribers</span>', chan_seg)
        sub_raw = m.group(1) if m is not None else "-1"
        if sub_raw[-1] == "M":
            sub_c = float(sub_raw[:-1])*1000000
        elif sub_raw[-1] == "K":
            sub_c = float(sub_raw[:-1])*1000
        else:
            sub_c = float(sub_raw)
        sub_l.append((chan_id, chan_name, str(sub_c)))
    return sub_l
