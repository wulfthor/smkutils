#!/usr/bin/python

# -*- encoding: utf-8 -*-
# TODO
# https://dev.twitter.com/rest/public/timelines
# for pagination

from __future__ import unicode_literals
import requests
import urllib2
import json
import sys, getopt
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "hyRu"
CONSUMER_SECRET = "tp5wfQEsYK"

OAUTH_TOKEN = "113UNavE4jAPNxo"
OAUTH_TOKEN_SECRET = "eZNA0fSw"




def main():

        count=20
        method="searcht"
        filelocation="/tmp/test.txt"
        test=0
        lang="da"

        try:
                opts, args = getopt.getopt(sys.argv[1:],"s:u:m:c:ta:f:")
                for o, a in opts:
                        if o == "-s":
                                searchstring = urllib2.quote(a.encode('utf8'))
                        elif o == "-u":
                                user = a
                        elif o == "-m":
                                method = a
                        elif o == "-c":
                                count = a
                        elif o == "-t":
                                test = 1
                        elif o == "-f":
                                filelocation = a
                        elif o == "-l":
                                lang = a
                        else:
                                assert False, "unhandled option"

        except getopt.GetoptError as err:
                print(err)
                sys.exit(2)

        fh = open(filelocation,"a")
        fh.write(" ------")
        fh.write("\n")
        
        baseurl="https://api.twitter.com/1.1/"
        #http://api.twitter.com/1.1/users/search.json
        if method == "searchu":
                myurl=baseurl + "users/search.json?q=" + user + "&result_type=mixed&count=" + str(count)
        if method == "searcht":
                #myurl=baseurl + "get/search/tweets.json?q=%23" + user
                #myurl=baseurl + "get/search/tweets.json?q=&from=" + user + "&count=100"
                #myurl=baseurl + "search/tweets.json?q=@noradio"
                #myurl=baseurl + "search/tweets.json?q=wulfthor&result_type=mixed&count=4"
                myurl=baseurl + "search/tweets.json?q=" + searchstring + "&lang=" + lang + "&count=" + str(count)
        if method == "timeline":
                myurl=baseurl + "statuses/user_timeline.json?" + "screen_name=" + user + "&count=" + str(count)

        fh.write(myurl)
        r = requests.get(url=myurl, auth=oauth)
        #print json.dumps(input, sort_keys = False, indent = 4)
        #print json.dumps(r,sort_keys = False, indent = 4)
        newdata = json.loads(r.text)
        if test:
                print json.dumps(newdata, sort_keys=True, indent=4)
                print "------------------"
                #print newdata
        count=0
        print len(newdata)
        if method == "timeline":
                for row in newdata[0]:
                        print (newdata[count]['text'].encode('utf8'))
                        fh.write(newdata[count]['text'].encode('utf8'))
                        #fh.write(str(newdata[count]['text'].encode('utf8')))
                        #fh.write(str(newdata[count]['text'].encode('utf8')))
                        #fh.write("\n")
                        count=count+1
        elif method == "searcht":
                for k in newdata['statuses']:
                        print k['text'].encode('utf8')
                        if  k['user']['entities']:
                                if  k['user']['entities'].get('url'):
                                        print k['user']['entities']['url']['urls'][0]['expanded_url']
                        #print k['user']['entities']['url']['urls'][0]['expanded_url']
                        #print (newdata['statuses'][count]['text'].encode('utf8'))
                        fh.write("\n")
        count=count+1


        fh.close()


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finnally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
        oauth = get_oauth()
        main()
        #r = requests.get(url="https://api.twitter.com/1.1/statuses/mentions_timeline.json", auth=oauth)
        #r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q=%23freebandnames&since_id=22619984051000&max_id=250126199840518145&result_type=mixed&count=4", auth=oauth)
