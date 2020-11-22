from scrape_video import Scraper

scraper = Scraper()
#commenter_subs = scraper.scrape_commenter_subs("UC7ZUmtySp0bx2lw_1VGw3Yg")
#print(commenter_subs)
comments = scraper.scrape_commenters("-SaPhS9c5Fw")
print(comments)
