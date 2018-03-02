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

from __future__ import print_function
from sys import version_info

import oauth2 as oauth
import urllib, json

from collections import namedtuple


class Client:        

    def __init__(self, account, secret, debug=False):
        self.account = str(account)
        self.host = "http://api.sugestio.com"
        self.debug = debug
        self.client = oauth.Client(oauth.Consumer(account, secret))

    def add_user(self, user):
        url = self._base() + "/users.json"
        return self._do_post(url, user)

    def add_users(self, users):
        url = self._base() + "/users.json"
        self._add_bulk(url, users, 20)

    def add_item(self, item):
        url = self._base() + "/items.json"
        return self._do_post(url, item)

    def add_items(self, items):
        url = self._base() + "/items.json"
        self._add_bulk(url, items, 20)

    def add_consumption(self, consumption):
        url = self._base() + "/consumptions.json"
        return self._do_post(url, consumption)

    def add_consumptions(self, consumptions):
        url = self._base() + "/consumptions.json"
        self._add_bulk(url, consumptions, 100)

    def _add_bulk(self, url, objects, chunksize=10):
        chunks = [objects[x:x + chunksize] for x in range(0, len(objects), chunksize)]
        i = 0
        for chunk in chunks:
            i = i + 1
            attempt = 0
            success = False
            print("chunk", i, "of", len(chunks))
            while success == False and attempt < 3:
                attempt = attempt + 1
                status, content = self._do_post(url, chunk)
                if status == 202:
                    success = True
                    print("\tattempt", attempt, "returned status", status, "(Accepted)")
                elif status >= 400 and status < 500:
                    success = True
                    print("\tattempt", attempt, "returned status", status, "(user error):", content)
                else:
                    print("\tattempt", attempt, "returned status", status, "(service error):",
                          content)

    def get_user_consumptions(self, userid, itemid=None):
        url = self._base() + "/users/" + Client._xstr(userid) + "/consumptions"
        if not itemid is None:
            url = url + "/" + Client._xstr(itemid)
        url = url + ".json"
        return self._do_get(url)

    def get_recommendations(self, userid, limit=None):
        url = self._base() + "/users/" + Client._xstr(userid) + "/recommendations.json"
        params = {}
        if not limit is None:
            params['limit'] = limit
        return self._do_get(url, params)

    def get_similar(self, itemid):
        url = self._base() + "/items/" + Client._xstr(itemid) + "/similar.json"
        return self._do_get(url)

    def _get_recommendations_or_similar(self, url, params={}):
        return self._do_get(url, params)

    def get_item(self, itemid):
        url = self._base() + "/items/" + Client._xstr(itemid) + ".json"
        return self._do_get(url)

    def get_user(self, userid):
        url = self._base() + "/users/" + Client._xstr(userid) + ".json"
        return self._do_get(url)

    def get_consumption(self, consumptionid):
        url = self._base() + "/consumptions/" + Client._xstr(consumptionid) + ".json"
        return self._do_get(url)

    def delete_item(self, itemid):
        url = self._base() + "/items/" + Client._xstr(itemid) + ".json"
        return self._do_delete(url)

    def delete_user(self, userid):
        url = self._base() + "/users/" + Client._xstr(userid) + ".json"
        return self._do_delete(url)

    def delete_consumption(self, consumptionid):
        url = self._base() + "/consumptions/" + Client._xstr(consumptionid) + ".json"
        return self._do_delete(url)

    def delete_user_consumptions(self, userid, itemid=None):
        url = self._base() + "/users/" + Client._xstr(userid) + "/consumptions"
        if not itemid is None:
            url = url + "/" + Client._xstr(itemid)
        url = url + ".json"
        return self._do_delete(url)

    def _do_get(self, url, params={}):
        verb = 'GET'
        if len(params) > 0:
            try:
                # python 3.x
                querystring = urllib.parse.urlencode(params)
            except AttributeError:
                # python 2.x fallback
                querystring = urllib.urlencode(params)
            url = url + "?" + querystring
        if self.debug:
            print(verb, url)
        resp, content = self.client.request(url, verb)

        if version_info[0] > 2:
            content = str(content, "utf-8")

        if resp['status'] == '200':
            objects = Client._json2obj(content)
            return int(resp['status']), objects
        else:
            return int(resp['status']), content

    def _do_post(self, url, object):
        verb = 'POST'
        headers = {'Content-Type':'application/json'}
        body = json.dumps(object, default=Client._serialize)
        if version_info[0] > 2:
            body = bytes(body, "utf-8")
        if self.debug:
            print(verb, url)
        response, content = self.client.request(url, verb, body=body, headers=headers)
        if version_info[0] > 2:
            content = str(content, "utf-8")
        return int(response['status']), content

    def _do_delete(self, url):
        verb = 'DELETE'
        if self.debug:
            print(verb, url)
        response, content = self.client.request(url, verb)
        if version_info[0] > 2:
            content = str(content, "utf-8")
        return int(response['status']), content

    @staticmethod
    def _xstr(s):
        if s is None:
            return ''
        return str(s)

    @staticmethod
    def _serialize(obj):
        return obj.__dict__

    @staticmethod
    def _json2obj(data):
        return json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

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
    item = None


class Consumption:

    def __init__(self, userid, itemid):
        self.userid = userid
        self.itemid = itemid

    id = None
    userid = None
    itemid = None
    type = None
    detail = None
    date = None


class Item:

    def __init__(self, id):
        self.id = id
        self.category = []
        self.tag = []
        self.creator = []
        self.segment = []

    title = None
    permalink = None
    location_latlong = None

class User:

    def __init__(self, id):
        self.id = id

    gender = None
    birthday = None