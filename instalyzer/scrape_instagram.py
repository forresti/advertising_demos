

# sudo pip install -U selenium    #worked out of the box.

from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import os
from IPython import embed
import forrestRequests
import instalyzer_core as insta


imgDir = './images'
if not os.path.exists(imgDir):
    os.mkdir(imgDir)

accounts = ['americanair', 'apple', 'sony', 'nike', 'merrelloutside', 'headtennis']
#accounts = ['tillythelab', 'cosmotheborador'] #dogs
driver = webdriver.Firefox()
for acc in accounts:
    pageUrl = 'http://instagram.com/' + acc
    print pageUrl

    imgDir_thisPage = imgDir + '/' + acc  # e.g. ./images/americanair
    insta.pull_images_instagram(pageUrl, imgDir_thisPage, driver)
 
driver.close()

