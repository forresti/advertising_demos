
import sys
import time
import urllib2

#def robustRequest_image(proxyList, url):
def robustRequest_image(url, outDir):
    headers={'User-agent' : 'Mozilla/5.0', 'Referer' : 'http://www.instagram.com'}
    timeout = 8 #seconds
    num_retries = 10
    outFilename = outDir + '/' + url.split('/')[-1] #-1 to get last element in list

    for i in xrange(0,num_retries):
        #proxy = randomProxy(proxyList)
        #handler = urllib2.ProxyHandler(proxy)

        #handler = urllib2.BaseHandler()
        #opener = urllib2.build_opener(handler, urllib2.HTTPHandler(debuglevel=0))
        #urllib2.install_opener(opener)

        req = urllib2.Request(url, None, headers)
        try:
            with open(outFilename, "wb") as local_file: #http://stackoverflow.com/questions/4028697
                local_file.write(urllib2.urlopen(req, None, timeout).read())

            #print "success for proxy %s"%proxy
            return
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print "exeption %s for url %s" %(sys.exc_info()[0], url)
            #print "timeout for %s" %url
            #print "timeout for proxy %s"%proxy
    print "unable to pull url %s"%url


