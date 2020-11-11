import sys
import time
import os
import random
import datetime
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def parse_comments(html):
    # Parsing comments
    comment_l = []
    for comment_section in html.split('<a id="author-text" class="yt-simple-endpoint style-scope ytd-comment-renderer"')[1:]:
        # Author
        m = re.search('href="/channel/([^\"]*)"', comment_section)
        if m is None: continue
        author_channel = m.group(1)
        # Comment
        if '<span dir="auto" class="style-scope yt-formatted-string">' in comment_section:
            comment = " ".join([m.group(1).strip().replace("\t", " ") for m in re.finditer('<span dir="auto" class="style-scope yt-formatted-string">([^\<]*)<', comment_section)])
        else:
            m = re.search('id="content-text" slot="content" split-lines="" class="style-scope ytd-comment-renderer">([^\<]*)<', comment_section)
            comment = m.group(1).strip().replace("\t", " ") if m is not None else ""
        comment = comment.replace("\n", " ")
        # Likes
        m = re.search('<span id="vote-count-left" class="style-scope ytd-comment-action-buttons-renderer" hidden="" aria-label="([^\"]*)">', comment_section)
        likes_c = 0
        if m is not None:
            likes_raw_str = m.group(1).split(" ")[0]
            try:
                if likes_raw_str[-1] == "K":
                    likes_c = int(float(likes_raw_str[:-1])*1000)
                elif likes_raw_str[-1] == "M":
                    likes_c = int(float(likes_raw_str[:-1])*1000000)
                else:
                    likes_c = int(likes_raw_str)
            except:
                print("ERROR - Parsing Likes:", m.group(1))
        comment_l.append((author_channel, comment, str(likes_c)))
    return comment_l

def get_comment_count(html):
    if "style-scope ytd-comment-renderer" in html:
        no_comments_c = 0
        # Estimate number of comments
        num_coms = len(html.split("</yt-formatted-string><yt-formatted-string id")) - 1
        return num_coms
    else:
        return 0
