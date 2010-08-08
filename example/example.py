import sugestio

if __name__ == "__main__":

    client = sugestio.Client('sandbox', 'demo')
    status, content = client.get_recommendations(1)

    if status == 200:
        print content[0].itemid
        print content[0].score
        print content[0].algorithm
    else:
        print "server response code =", status
        print content



    