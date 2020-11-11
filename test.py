from scrape_video import Scraper

scraper = Scraper()
# scraper.scrape_commenter_subs("./txt/commenters.txt", "./txt/commenter_subs.txt")

scraper.scrape_commenters("./txt/videos.txt", "./txt/video_commenters.txt")
