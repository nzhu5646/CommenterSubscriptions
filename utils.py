import re

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

def parse_recommended(html):
    rec_l = []
    # Parsing recommended videos
    for rec_section in html.split('<ytd-compact-video-renderer class="style-scope ytd-watch-next-secondary-results-renderer"')[1:]:
        # Video title
        m = re.search('title="(.*)"', rec_section)
        if m is None: continue
        video_title = m.group(1)

        # Video Link
        m = re.search('href="\/watch\?v=(.*)"', rec_section)
        if m is None: continue
        video_uri = m.group(1)

        # Channel name
        m = re.search('ytd-channel-name" ellipsis-truncate="">(.*)<\/yt-formatted-string>', rec_section)
        if m is None: continue
        channel_name = m.group(1)

        # Views
        m = re.search('<span class="style-scope ytd-video-meta-block">(.*) views', rec_section)
        if m is None: continue
        views = m.group(1)

        # Time
        m = re.search('<span class="style-scope ytd-video-meta-block">(.*) ago', rec_section)
        if m is None: continue
        time = m.group(1)

        rec_l.append((video_title, video_uri, channel_name, views, time))
    return rec_l

def get_recommended_count(html):
    if "style-scope ytd-compact-video-renderer" in html:
        no_rec_c = 0
        # Estimate number of recommended videos
        num_rec = len(html.split("<ytd-compact-video-renderer")) - 1
        return num_rec
    else:
        return 0
