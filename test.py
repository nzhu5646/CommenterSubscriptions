from scrape_video import Scraper

scraper = Scraper(headless=True)

# commenter_featured = scraper.scrape_channel_featured(["UC7ZUmtySp0bx2lw_1VGw3Yg"])
# print(commenter_featured)

comments = scraper.scrape_comments(["-SaPhS9c5Fw", "MClIOo_zS9Q"], 15)
print(comments)
#
# recommended = scraper.scrape_recommended(["MClIOo_zS9Q"])
# print(recommended)
