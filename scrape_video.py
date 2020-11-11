import re
import sys
import time
import os
import random
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrape_comments_local import parse_comments, get_comment_count
from scrape_commenter_subs_local import parse_subs

class Scraper():

    """ NOTE WILL NOT WORK IF CHANNEL IS IDENTIFIED BY USERNAME """
    def scrape_commenter_subs(self, input, output):
        driver = webdriver.Chrome()

        # Make file if doesn't exist, otherwise collect previously scraped channels
        out_fp = output
        already_scraped_s = set([])
        if not os.path.exists(out_fp):
            of = open(out_fp, "w")
        else:
            for line in open(out_fp):
                already_scraped_s.add(line.split("\t")[0])
            of = open(out_fp, "a")

        print("Already scraped: ", len(already_scraped_s))

        commenter_fp = input
        chan_id_l = [l.strip() for l in open(commenter_fp)]
        random.shuffle(chan_id_l)

        no_sub_c = 0
        for channel_id in chan_id_l:
            if channel_id == "" or channel_id in already_scraped_s:
                continue
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
                html = driver.page_source.encode("ascii", "ignore").decode()
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
            # Keep track of number of times in a row no subs were found
            if num_subs == 0:
                no_sub_c += 1
            else:
                no_sub_c = 0
            # Output ALL subs data
            print(datetime.datetime.now())
            already_scraped_s.add(channel_id)
            sub_l = parse_subs(last_inc_html)
            if not sub_l:
                of.write("\t".join([channel_id, "", "", ""]) + "\n")
            else:
                for tpl in sub_l:
                    of.write("\t".join((channel_id,) + tpl) + "\n")
            # Stop if continuing to fail
            if no_sub_c >= 15:
                #scrape_email_util.send_email(aws_access_key_id, aws_secret_access_key, "SUB SEL SCRAPE FINISHED - FAILED - " + commenter_fp, commenter_fp)
                os.system("touch %(out_fp)s.FAILED" % vars())
                of.close()
                sys.exit(1)
                break


        of.close()
        driver.close()

    def scrape_commenters(self, input, output):
        driver = webdriver.Chrome()

        comments_fp = output

        if os.path.exists(comments_fp):
            already_scraped_s = set([l.split("\t")[1] for l in open(comments_fp)])
            comments_f = open(comments_fp, "a")
        else:
            already_scraped_s = set([])
            comments_f = open(comments_fp, "w")
        print("Already scraped: ", len(already_scraped_s))

        vid_fp = input
        vid_id_l = [l.strip("\n").split("\t") for l in open(vid_fp)]
        random.shuffle(vid_id_l)

        no_comments_c = 0
        success = True
        for channel_id, video_id in vid_id_l:
            if video_id == "" or video_id in already_scraped_s:
                continue
            url = "https://www.youtube.com/watch?v=" + video_id
            print("Scraping:", url)
            driver.get(url)
            time.sleep(3)
            com_c = 0
            last_com_c = 0
            no_improvement = 0
            for i in range(10):
                scroll_amount = str((i+1)*500)
                driver.execute_script("window.scrollTo(0, %(scroll_amount)s);" % vars())
                time.sleep(2)
                html = driver.page_source.encode("ascii", "ignore").decode()
                com_c = get_comment_count(html)
                print(no_improvement, com_c)
                if com_c == last_com_c:
                    no_improvement += 1
                else:
                    no_improvement = 0
                if no_improvement >= 2:
                    break
                last_com_c = com_c
            # Keep track of number of videos with no comments in a row
            if com_c > 0:
                no_comments_c = 0
            else:
                no_comments_c += 1
                print("NO COMMENTS: ", no_comments_c)
            """
            # Output ALL data for now
            ofp = out_dir + "/" + video_id + ".html"
            of = open(ofp, "w")
            of.write(html)
            of.close()
            os.system("gzip " + ofp)
            """
            # Parse and output results
            for author_channel, comment, likes in parse_comments(html):
                comments_f.write("\t".join([channel_id, video_id, author_channel, comment, likes]) + "\n")
            print(datetime.datetime.now())
            already_scraped_s.add(video_id)
            if no_comments_c >= 20:
                os.system("touch %(comments_fp)s.FAILED" % vars())
                scrape_email_util.send_email(aws_access_key_id, aws_secret_access_key, "COMMENT SCRAPE FINISHED - FAILED - " + vid_fp, vid_fp)
                success = False
                break

            driver.close()
            comments_f.close()
