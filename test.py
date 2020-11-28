from scrape_video import Scraper

scraper = Scraper(headless=True)

# commenter_featured = scraper.scrape_commenter_featured("UC7ZUmtySp0bx2lw_1VGw3Yg")
# print(commenter_featured)
#
# comments = scraper.scrape_commenters("-SaPhS9c5Fw")
# print(comments)

recommended = scraper.scrape_recommended("-SaPhS9c5Fw")
print(recommended)
