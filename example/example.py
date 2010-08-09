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

def add_item():

    params = {'id':'X75FKGE-E', 'from':'2010-07-01', 'until':'2010-09-01'}
    params['tag'] = ['tag1', 'tag2']
    status = client.add_item(params)

    print "server response code:", status

if __name__ == "__main__":

    get_recommendations()
    #add_consumption()
    #add_user()
    #add_item()
    print "Done."