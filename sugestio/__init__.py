"""
The MIT License

Copyright (c) 2010 Sugestio.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sugestio
import oauth2 as oauth
import urllib
import csv
import sys

class Client:        

    def __init__(self, account, secret):
        self.account = str(account)
        self.host = "http://api.sugestio.com"
        self.client = oauth.Client(oauth.Consumer(account, secret))
        self.multivalued = set(['category', 'creator', 'segment', 'tag'])


    def add_user(self, user):
        url = self._base() + "/users"
        resp, content = self._do_post(url, user)
        return int(resp['status'])


    def add_item(self, item):
        url = self._base() + "/items"
        resp, content = self._do_post(url, item)        
        return int(resp['status'])


    def add_consumption(self, consumption):
        url = self._base() + "/consumptions"        
        resp, content = self._do_post(url, consumption)
        return int(resp['status'])


    def get_recommendations(self, userid):
        url = self._base() + "/users/" + str(userid) + "/recommendations.csv"        
        return self._get_recommendations_or_similar(url)
    

    def get_similar(self, itemid):
        url = self._base() + "/items/" + str(itemid) + "/similar.csv"
        return self._get_recommendations_or_similar(url)


    def _get_recommendations_or_similar(self, url):
        resp, content = self.client.request(url, "GET")

        if resp['status'] == '200':
            recommendations = self._parse(content)
            return int(resp['status']), recommendations
        else:
            return int(resp['status']), content

    def _do_post(self, url, parameters):        
        body = urllib.urlencode(self._flatten(parameters))
        return self.client.request(url, "POST", body)

    def _flatten(self, dictionary):
        flattened = {}

        for k, v in dictionary.items():
            if k in self.multivalued:
                i = 0
                for x in v:
                    newkey = "%s[%i]" % (k,i)
                    flattened[newkey] = x
                    i = i + 1
            else:
                flattened[k] = v

        return flattened

    def _parse(self, content):
        recommendations = []
        reader = csv.reader(content.split("\n"))

        for row in reader:
            try:
                recommendations.append(sugestio.Recommendation(row[0], row[1], row[2]))
            except:
                pass #print sys.exc_info()[0]

        return recommendations

    def _base(self):
        return self.host + "/sites/" + self.account


class Recommendation:

    def __init__(self, itemid, score, algorithm):
        self.itemid = itemid
        self.score = score
        self.algorithm = algorithm

    itemid = None
    score = None
    algorithm = None
