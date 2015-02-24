#!/usr/bin/python

import sys
import base64
import pdb
import codecs
import urllib2
import urllib
import re
import json

reload(sys);
sys.setdefaultencoding("utf8")

########################################################
# usage:
#   getSolr.py 1920 3 1920
#   getSolr.py <before> <count> <fromD>
#
# if fromD not empty its dead later than fromD
# cat /tmp/on6 | jq '.[] | {m: .docs[].title_eng, p: [.docs[].acq_method]}'
# :
# curl http://solr.smk.dk:8080/solr/prod_all_dk/select?q=artist_name:Haugen\&wt=json\&rows=10\&indent=true -s
# curl http://solr.smk.dk:8080/solr/prod_all_dk/select?q=artist_death_dk:%5B%2A+TO+1920%5D\&wt=json\&rows=10\&indent=true
# simple wrapper function to encode the username & pass

formD=0
server='solr'
response=''
count=sys.argv[2]
before=sys.argv[1]
fromD=sys.argv[3]
fh=open('/tmp/xtest','a')

#url = 'http://cstest.smk.dk:8180/cspace-services/blobs/6c6e0e0d-2460-413a-840e/derivatives/Medium/content'
#url='http://cstest.smk.dk:8180/cspace-services/collectionobjects?kw=Kobber'
params={}
params['artist_death_dk']='[* TO '+before+']'
if fromD != 0:
  params['artist_death_dk']='['+fromD+' TO *]'
npar = urllib.urlencode(params)
tpar = npar.replace("=",":")
url='http://'+server+'.smk.dk:8080/solr/prod_all_dk/select?q='+tpar+'&wt=json&rows='+count+'&indent=true'

#req.add_header("Content-Length", "32000")
#req.add_header("Content-transfer-Encoding", "binary")
#req.add_header("Content-Type", "text/html")
try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
except urllib2.URLError, e:
        fh.write("1sdf\n")
        fh.write(str(e.reason))
        fh.write("1sdf\n")
except urllib2.HTTPError, e:
        fh.write("2sdf\n")
        fh.write(e.args)
except httplib.HTTPException, e:
        fh.write("3sdf\n")
        fh.write(e.args)
except Exception:
        fh.write("4sdf\n")
        import traceback
        fh.write('generic exception: ' + traceback.format_exc())
except urllib2.URLError, e:
        print e.code
except urllib2.HTTPE, e:
        print e.args

print response.read()
