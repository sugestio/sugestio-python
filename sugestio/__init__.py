import sugestio
import oauth2 as oauth
import csv
import sys

class Client:    

    def __init__(self, account, secret):

        self.account = str(account)
        self.host = "http://api.sugestio.com"
        self.client = oauth.Client(oauth.Consumer(account, secret))

    def add_user(self, user):
        pass

    def add_item(self, item):
        pass

    def add_consumption(self, consumption):
        pass

    def get_recommendations(self, userid):

        url = self.__base() + "/users/" + str(userid) + "/recommendations.csv"
        method = "GET"
        resp, content = self.client.request(url, method)                

        if resp['status'] == '200':
            recommendations = self.__parse(content)
            return int(resp['status']), recommendations
        else:
            return int(resp['status']), content


    def get_similar(self, itemid):

        url = self.__base() + "/items/" + str(itemid) + "/similar.csv"
        method = "GET"
        resp, content = self.client.request(url, method)

        if resp['status'] == '200':
            recommendations = self.__parse(content)
            return int(resp['status']), recommendations
        else:
            return int(resp['status']), content

    def __parse(self, content):

        recommendations = []
        reader = csv.reader(content.split("\n"))

        for row in reader:
            try:
                recommendations.append(sugestio.Recommendation(row[0], row[1], row[2]))
            except:
                pass

        return recommendations

    def __base(self):
        return self.host + "/sites/" + self.account


class Recommendation:

    def __init__(self, itemid, score, algorithm):
        self.itemid = itemid
        self.score = score
        self.algorithm = algorithm

    itemid = None
    score = None
    algorithm = None