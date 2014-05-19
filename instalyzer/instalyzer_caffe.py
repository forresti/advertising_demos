from caffe import imagenet
from matplotlib import pyplot
import pylab
import numpy as np
import os
from IPython import embed
import networkx as nx
import synsets_to_graph
import instalyzer_core as insta 

class InstalyzerCaffe:
    #MODEL_FILE = '/media/big_disk/installers_old/caffe_lowMemConv//examples/imagenet/imagenet_deploy.prototxt'
    MODEL_FILE = '/media/big_disk/installers_old/caffe_lowMemConv//examples/imagenet/imagenet_deploy_batch1.prototxt'
    PRETRAINED = 'thirdparty/alexnet_train_iter_470000'
    synset_word_file = 'thirdparty/synset_words.txt'

    #TODO: remove ancestorKeywords ... it's depricated and replaced by ancestorKeywords_dict.
    ancestorKeywords = ['conveyance, transport', #Travel, Cars, Airplanes... 
                        'electronic equipment', 
                        'iPod', 
                        'personal computer, PC, microcomputer',
                        'sports equipment', #Sports
                        'sports implement', #Sports
                        'food, solid food', 
                        'food, nutrient', 
                        'dog, domestic dog, Canis familiaris', #Pets
                        'cat, true cat', #Pets 
                        'geological formation, formation'] #based on relevance to online ad community

    # human-readable category list so far:
    #    Vehicles and Travel, Handheld Electronics, iPod, Computers, Sports, Food and Drink, Pets, Outdoors 
    # dictionary... {'imagenet high-level category' : 'human readable category'}
    ancestorKeywords_dict = {'conveyance, transport': 'Vehicles and Travel',
                        'electronic equipment': 'Handheld Electronics', 
                        'iPod': 'iPod', 
                        'personal computer, PC, microcomputer': 'Computers',
                        'sports equipment': 'Sports',
                        'sports implement': 'Sports',
                        'food, solid food': 'Food and Drink', 
                        'food, nutrient': 'Food and Drink', 
                        'dog, domestic dog, Canis familiaris': 'Pets', 
                        'cat, true cat': 'Pets',
                        'geological formation, formation': 'Outdoors'}

    gr = synsets_to_graph.get_graph() #imagenet graph as a networkx object
    center_only = True #don't do the 10-crops thing

    def __init__(self):
        self.net = imagenet.ImageNetClassifier(self.MODEL_FILE, self.PRETRAINED, self.center_only) #the primary object in this class
        self.net.caffenet.set_phase_test()
        self.net.caffenet.set_mode_cpu()
        [self.synset_WNIDs, self.synset_words] = synsets_to_graph.load_synset_words(self.synset_word_file)

    #TODO: make instagram_predict take an ARRAY of filenames.
    # run Caffe and record the top-5 predictions
    def instagram_predict(self, IMAGE_FILE):
        predictions = self.net.predict(IMAGE_FILE) # 1000-d softmax scores for imagenet 1k
        #pyplot.plot(predictions)
        #pylab.savefig('predictions.jpg')

        sortedPredictions = np.argsort(predictions) #keys 0 to 999, sorted by ascending prediciton score
        sortedPredictions = sortedPredictions[::-1] #reverse array (descending order now)
        topPred = sortedPredictions[0:5] #descending order of confidence
        topPredName = [self.synset_words[x] for x in topPred]
        return topPredName

    # @param topPredName = top few (typically 5) categories predicted for an image. in english (e.g. 'digital computer')
    def check_relevant_ancestors(self, topPredName):
        found_relevant_ancestors = []
        for className in topPredName: #top few predicted classes
            newAncestors = nx.dag.ancestors(self.gr, className)
            for anc in newAncestors:
                if anc in self.ancestorKeywords_dict.keys():
                    #found_relevant_ancestors.append(anc) #imagenet nomenclature (e.g. sports equipment)
                    anc_readable = self.ancestorKeywords_dict[anc]
                    found_relevant_ancestors.append(anc_readable) #e.g. Sports

        found_relevant_ancestors = list(set(found_relevant_ancestors)) #remove duplicates
        return found_relevant_ancestors


'''
# EXAMPLE USAGE:
#instacaffe = instalyzer_caffe.InstalyzerCaffe()
instacaffe = InstalyzerCaffe()
image_files = insta.get_image_files()
pred = instacaffe.instagram_predict(image_files[0])
print pred
found_relevant_ancestors = instacaffe.check_relevant_ancestors(pred)
print found_relevant_ancestors
'''

