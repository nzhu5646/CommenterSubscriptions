import re
import sys
import time
import os
import random
import datetime
import utils

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scraper():
    def __init__(self, headless=False, driver=None):
        self.driver_path = driver
        self.headless = headless

    """
    Given a channel URI, will crawl through the list of featured channels and
    compile into a list. Will attempt to get the first 1000 subscribers.
    Input: Channel URI
    Output: List of featured channel dictionaries each with the fields (channel_uri, channel_name, num_subscribers)
    Note: Used to list the channel's subscriptions
    instead of the channel's featured channels.
    """
    def scrape_commenter_featured(self, channel_id):
        options = None
        if self.headless:
            options = Options()
            options.headless = True

        if self.driver_path:
            driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        else:
            driver = webdriver.Chrome(chrome_options=options)


        url = "https://www.youtube.com/channel/" + channel_id + "/channels"
        print("Scraping:", url)
        driver.get(url)
        time.sleep(3)
        # Scroll until no new subs are found for 2 scrolls
        fail_inc_c = 0
        scroll_c = 0
        last_sub_c = 0
        last_inc_html = ""
        while fail_inc_c < 2:
            scroll_amount = str((scroll_c+1)*20000)
            driver.execute_script("window.scrollTo(0, %(scroll_amount)s);" % vars())
            time.sleep(2)
            html = driver.page_source.encode("utf-8").decode()
            num_subs = len(html.split('<div id="channel" class="style-scope ytd-grid-channel-renderer">'))
            if num_subs < last_sub_c:
                break
            elif num_subs == last_sub_c:
                fail_inc_c += 1
            else:
                last_inc_html = html
                fail_inc_c = 0
            scroll_c += 1
            last_sub_c = num_subs
            print(scroll_c, fail_inc_c, num_subs)
            if num_subs >= 1000:
                break

        # Output ALL subs data
        print(datetime.datetime.now())
        sub_l = utils.parse_subs(last_inc_html)

        driver.close()

        return sub_l

    """
    Given a video URI, will attempt to scrape comments and metadata from comment section.
    Input: Video URI
    Output: List of dictionaries each with the following fields (author_channel, comment, num_likes)
    """
    def scrape_commenters(self, video_id):
        options = None
        if self.headless:
            options = Options()
            options.headless = True

        if self.driver_path:
            driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        else:
            driver = webdriver.Chrome(chrome_options=options)

        url = "https://www.youtube.com/watch?v=" + video_id
        print("Scraping:", url)
        driver.get(url)
        time.sleep(10)
        com_c = 0
        last_com_c = 0
        no_improvement = 0
        for i in range(10):
            scroll_amount = str((i+1)*500)
            driver.execute_script("window.scrollTo(0, %(scroll_amount)s);" % vars())
            time.sleep(10)
            html = driver.page_source.encode("utf-8").decode()
            com_c = utils.get_comment_count(html)
            print(no_improvement, com_c)
            if com_c == last_com_c:
                no_improvement += 1
            else:
                no_improvement = 0
            if no_improvement >= 2:
                break
            last_com_c = com_c

        # Parse and output results
        test_file = open("test_good.txt", "w")
        test_file.write(html)
        comments = utils.parse_comments(html)
        print(datetime.datetime.now())

        driver.close()

        return comments

    """
    Given a video URI, will attempt to scrape recommended videos
    Input: Video URI
    Output: List of dictionaries each with the following fields (title, video_uri, channel_name, num_views, publish_date, timestamp)
    """
    def scrape_recommended(self, video_id):
        options = None
        if self.headless:
            options = Options()
            options.headless = True

        if self.driver_path:
            driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        else:
            driver = webdriver.Chrome(chrome_options=options)

        url = "https://www.youtube.com/watch?v=" + video_id
        print("Scraping:", url)
        driver.get(url)
        time.sleep(3)
        rec_c = 0
        last_rec_c = 0
        no_improvement = 0
        for i in range(10):
            scroll_amount = str((i+1)*500)
            driver.execute_script("window.scrollTo(0, %(scroll_amount)s);" % vars())
            time.sleep(2)
            html = driver.page_source.encode("utf-8").decode()
            rec_c = utils.get_recommended_count(html)
            print(no_improvement, rec_c)
            if rec_c == last_rec_c:
                no_improvement += 1
            else:
                no_improvement = 0
            if no_improvement >= 2:
                break
            last_rec_c = rec_c

        # Parse and output results
        recommended = utils.parse_recommended(html)
        print(datetime.datetime.now())

        driver.close()

        return recommended
