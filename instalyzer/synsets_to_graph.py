
import networkx as nx
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
from IPython import embed

def mat_to_graph(synsets_mat):

    synGraph = nx.DiGraph()
  
    #embed() #aka 'keyboard'

    #nameIdx = 1; #for a synset entry, element 1 is the name (e.g. English setter)
    #childrenIdx = 7 #for a synset entry, element 1 is the list of children (e.g. [200, 302, ...])
 
    #add all nodes
    for nodeID in xrange(0, len(synsets_mat)):
        name = synsets_mat['words'][nodeID][0][0]
        nodeWNID = synsets_mat['WNID'][nodeID][0][0] #wordnet ID (e.g. n13809207)
        #print name
        synGraph.add_node(name, ID=nodeID, WNID=nodeWNID)

    #add all connections
    for nodeID in xrange(0, len(synsets_mat)):
        parentName = synsets_mat['words'][nodeID][0][0]
        children = synsets_mat['children'][nodeID][0][0]
        #print children
        for childID in children: 
            childName = synsets_mat['words'][childID-1][0][0] # -1 to account for matlab one-indexing
            #print '    %d' %childID 
            #print childName
            synGraph.add_edge(parentName, childName)

    return synGraph


def visualize_graph_(carGraph):
    #draw with NetworkX
    plt.figure(figsize=(30,5)) #default figsize=(8,6)
    pos=nx.graphviz_layout(carGraph,prog='dot') #thanks: stackoverflow.com/questions/11479624
    nx.draw(carGraph, pos, arrows=False, font_size=5)  #trying to make oval-shaped nodes with optional kwd: node_shape=(5,1)
    plt.show()
    plt.savefig("nx_graph.pdf")

    #draw with Dot
    A = nx.to_agraph(carGraph)
    #A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
    A.layout('dot', args='-Nwidth=".2" -Nheight=".2"')
    A.draw('synsets_imagenet1k_graph.pdf')

def visualize_graph():
    synsets_mat = sio.loadmat('thirdparty/ilsvrc1k_meta.mat')
    synsets_mat = synsets_mat['synsets']
    synsets_graph = mat_to_graph(synsets_mat)
    visualize_graph_(synsets_graph) #TODO: allow user-selectable output filename for saving the graph.

def get_graph():
    synsets_mat = sio.loadmat('thirdparty/ilsvrc1k_meta.mat')
    synsets_mat = synsets_mat['synsets']
    synsets_graph = mat_to_graph(synsets_mat)
    return synsets_graph

#thanks: http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/imagenet_pretrained.ipynb
# for imagenet 1k, this returns 1000 words, sorted in default order
# this is the same order that Caffe's softmax layer uses.
# unlike other functions in this file, load_synset_words() pulls its data from a .txt instead of a .mat.
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


