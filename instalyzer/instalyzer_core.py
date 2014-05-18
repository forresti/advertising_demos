from caffe import imagenet
from matplotlib import pyplot
import pylab
import numpy as np
import os
import time
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from IPython import embed
import networkx as nx
import synsets_to_graph
import forrestRequests

'''
#thanks: http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/imagenet_pretrained.ipynb
# for imagenet 1k, this returns 1000 words, sorted in default order
# this is the same order that Caffe's softmax layer uses.
def load_synset_words(synset_word_file):
    inF = open(synset_word_file, 'r')
    line = inF.readline()
    synset_words = []
    synset_WNIDs = []
    while(line):
        if len(line.split(",")) > 0:
            lineSplit = line.split(" ")
            WNID = lineSplit[0] # lineSplit[0] is ID (e.g. n01440764).
            synset_WNIDs.append(WNID.rstrip('\n').strip())
            #word = lineSplit[1] # linesplit[1:end] = dictionary word/synonyms
            begin_word_offset = len(WNID)+1 #beginning of dictionary word/synonyms in the string
            word = line[begin_word_offset:] #string after WNID
            synset_words.append(word.rstrip('\n').strip()) #remove newlines and whitespace
        line = inF.readline()
    return [synset_WNIDs, synset_words]
'''

def get_image_files():
    fileList = []
    for top, dirs, files in os.walk('./images'):
        for filename in files:
            filename_withdir = top + '/' + filename
            print filename_withdir
            fileList.append(filename_withdir)
    return fileList

#thanks: stackoverflow.com/questions/18130499/how-to-scrape-instagram-with-beautifulsoup
#for www.instagram.com (3/14/14)
def scrape_imgUrls_instagram(pageUrl, driver):
    driver.get(pageUrl)
    soup = BeautifulSoup(driver.page_source)

    imgUrls = [];
    for photoHtml in soup.findAll('li', {'class':'photo'}):
        imgUrl = None
        for currDiv in photoHtml.findAll('div'): # for the most part, each 'div' is an image or video
            if 'src' in currDiv.attrs: # a 'src' is typically a jpg 
                imgUrl = currDiv['src']
                break

        if imgUrl is not None:
            imgUrls.append(imgUrl)
            print '        ', imgUrl

    return imgUrls

# hard-coded out directory (could have user provide the out directory)
def pull_images_instagram(pageUrl, imgDir_thisPage, driver):
    start_time = time.time()
    print '    Scraping list of images from %s' %pageUrl
    imgUrls = scrape_imgUrls_instagram(pageUrl, driver)
    scrape_url_time = time.time() - start_time
    print '    Done scraping list of images (%f sec)' %scrape_url_time

    start_time = time.time()
    print '    Downloading images...'
    if not os.path.exists(imgDir_thisPage):
        os.mkdir(imgDir_thisPage)
    for url in imgUrls:
        forrestRequests.robustRequest_image(url, imgDir_thisPage)
    download_time = time.time() - start_time
    print '    Done downloading images (%f sec)' %download_time

