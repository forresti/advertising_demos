from caffe import imagenet
from matplotlib import pyplot
import pylab
import numpy as np
import os
from IPython import embed
import networkx as nx
import synsets_to_graph
import instalyzer_core as insta 
import instalyzer_caffe as instacaffe

# ITERATE OVER ALL IMAGES WE'VE SCRAPED -- ANALYZE THEIR CATEGORIES.

image_files = insta.get_image_files() #offline... pre-downloaded.
instanet = instacaffe.InstalyzerCaffe()

for f in image_files:
    print '    %s' %f
    #pred = insta.instagram_predict(net, f, synset_words)
    pred = instanet.instagram_predict(f) #TODO: run an array of image files
    print '        pred:', pred
    #found_relevant_ancestors = insta.check_relevant_ancestors(pred, ancestorKeywords, gr) 
    found_relevant_ancestors = instanet.check_relevant_ancestors(pred)
    print '        relevant ancestor categories:', found_relevant_ancestors
    print ""

