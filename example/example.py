import sugestio

ACCOUNT = 'sandbox'
SECRET = 'demo'

def recommendations():
    
    client = sugestio.Client(ACCOUNT, SECRET)
    status, content = client.get_recommendations(1)    

    if status == 200:
        print content[0].itemid
        print content[0].score
        print content[0].algorithm
    else:
        print "server response code =", status
        print content

def consumption():

    client = sugestio.Client(ACCOUNT, SECRET)

    params = {'userid':1, 'itemid':'abc', 'type':'VIEW'}
    status = client.add_consumption(params)

    print "server response code =", status


if __name__ == "__main__":

    #recommendations()
    consumption()
    