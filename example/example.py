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

ACCOUNT = 'sandbox'
SECRET = 'demo'

client = sugestio.Client(ACCOUNT, SECRET)


def get_recommendations():    
    status, content = client.get_recommendations(1)    

    if status == 200:
        print content[0].itemid
        print content[0].score
        print content[0].algorithm
    else:
        print "server response code:", status
        print content


def add_consumption():
    params = {'userid':1, 'itemid':'abc', 'type':'VIEW'}
    status = client.add_consumption(params)
    print "server response code:", status


def add_user():
    params = {'id':1, 'gender':'M', 'birthday':'1975-04-05'}
    status = client.add_user(params)
    print "server response code:", status


def delete_item_metadata():
    status = client.delete_item_metadata(1)
    print "server response code:", status


def delete_user_metadata():
    status = client.delete_user_metadata(1)
    print "server response code:", status


def delete_consumption():
    status = client.delete_consumption("a-b-c-1-2-3")
    print "server response code:", status


def delete_user_consumptions():
    status = client.delete_user_consumptions(1)
    print "server response code:", status


def add_item():
    params = {'id':'X75FKGE-E', 'from':'2010-07-01', 'until':'2010-09-01'}
    params['tag'] = ['tag1', 'tag2']
    status = client.add_item(params)
    print "server response code:", status


if __name__ == "__main__":

    #get_recommendations()
    #add_consumption()
    #add_user()
    #add_item()
    #delete_item_metadata()
    #delete_consumption()
    #delete_user_metadata()
    #delete_user_consumptions()
    print "Done."