from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import os
import sys
import time
from IPython import embed
from pyvirtualdisplay import Display
import forrestRequests
import instalyzer_core as insta
import instalyzer_caffe as instacaffe
from collections import Counter

# USAGE: python demo_instalyzer.py [optional: americanair]

#for headless mode, do: sudo apt-get install xvfb

# @param acc = instagram account name (e.g. merrelloutside)
def run_demo(acc):

    # INIT
    instanet = instacaffe.InstalyzerCaffe()

    # SCRAPE
    display = Display(visible=0, size=(800, 600)) #for headless mode
    display.start()
    driver = webdriver.Firefox() #show browser window
    #acc = 'merrelloutside' #TODO: take as cmd line arg
    pageUrl = 'http://instagram.com/' + acc
    imgDir = './images'
    if not os.path.exists(imgDir):
        os.mkdir(imgDir)
    imgDir_thisPage = imgDir + '/' + acc  # e.g. ./images/americanair
    insta.pull_images_instagram(pageUrl, imgDir_thisPage, driver) #SCRAPE INSTAGRAM
    driver.close()

    # ANALYZE
    print "    Analyzing images with deep learning..."
     
    start_time = time.time()
    #TODO: batch these images:
    high_level_categories = []
    pred = [] #low-level categories
    for f in os.listdir(imgDir_thisPage):
        currFname = imgDir_thisPage + '/' + f
        curr_pred = instanet.instagram_predict(currFname)
        curr_high_level = instanet.check_relevant_ancestors(curr_pred)
        pred = pred + curr_pred
        high_level_categories = high_level_categories + curr_high_level #append categories for current img

    #print high_level_categories
    category_freq = Counter(high_level_categories) #e.g. {'conveyance': 8, 'sports': 4, ...}
    cat_sort = list(reversed(sorted([ (c,v) for v,c in category_freq.iteritems() ]))) # flip dict and sort 
    #top_category = max(category_freq, key=category_freq.get) # TODO: get best 2 categories?

    analysis_time = time.time() - start_time #in sec

    print "    Done analyzing images (%f sec)" %analysis_time
    print "    we detected:    ", cat_sort[0:3]

if len(sys.argv) < 2: # argv[0] is the demo_instalyzer.py 
    run_demo('merrelloutside')
else: #one arg
    run_demo(sys.argv[1]) #user-selected instagram profile name

