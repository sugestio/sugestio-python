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
from sugestio import Client as SugestioClient
from sugestio import Consumption, Item, User

ACCOUNT = 'sandbox'
SECRET = 'secret'

client = SugestioClient(ACCOUNT, SECRET)


def get_recommendations():
    status, recommendations = client.get_recommendations(1, 2)

    if status == 200:
        print("Title\tScore")
        for recommendation in recommendations:
            print(recommendation.item.title + "\t" + str(recommendation.score))
    else:
        print("server response code:", status)
        print(recommendations)


def add_consumption():
    c = Consumption('1', 'abcd')
    c.type = "RATING"
    c.detail = "STAR:5:0:4"
    status, content = client.add_consumption(c)
    print("server response code:", status)


def get_consumption_history():
    status, consumptions = client.get_user_consumptions(35)
    if status == 200:
        for consumption in consumptions:
            print(consumption)
    else:
        print("server response code:", status)
        print(consumptions)


def add_user():
    u = User(10)
    u.gender = "M"
    u.birthday = "1975-04-05"
    status, content = client.add_user(u)
    print("server response code:", status)


def get_item_metadata():
    status, item = client.get_item(1)
    if status == 200:
        print ("Item:")
        print("\tId =", item.id)
        print("\tTitle =", item.title)
        print("\tCategories =")
        for c in item.category:
            print ("\t\t", c)
    else:
        print("Status", status, ":", item)


def delete_item_metadata():
    status, content = client.delete_item(15)
    print("server response code:", status)


def delete_user_metadata():
    status, content = client.delete_user(1)
    print("server response code:", status)


def delete_consumption():
    status, content = client.delete_consumption("a-b-c-1-2-3")
    print("server response code:", status)


def delete_user_consumptions():
    status, content = client.delete_user_consumptions(1)
    print("server response code:", status)


def add_item():
    item = Item('X75FKGE-E')
    item.title = 'Item X75FKGE-E'
    item.category.append('tag1')
    item.category.append('tag2')
    status, content = client.add_item(item)
    print("server response code:", status)


def add_items_bulk():
    items = []
    for i in range(1, 101):
        item = Item(i)
        item.title = "Item " + str(i)
        items.append(item)
    client.add_items(items)


if __name__ == "__main__":

    # get_recommendations()
    # add_consumption()
    # get_consumption_history()
    # add_user()
    # add_item()
    # add_items_bulk()
    # get_item_metadata()
    # delete_item_metadata()
    # delete_consumption()
    # delete_user_metadata()
    # delete_user_consumptions()
    print("Done.")
