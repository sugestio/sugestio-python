# Overview

This is a Python library for interfacing with the [Sugestio](http://www.sugestio.com) 
recommendation service. Data is submitted and retrieved in JSON format. The library uses
[python-oauth2](http://github.com/simplegeo/python-oauth2) to create the OAuth-signed requests. 

## About Sugestio

Sugestio is a scalable and fault tolerant service that now brings the power of 
web personalisation to all developers. The RESTful web service provides an easy to use 
interface and a set of developer libraries that enable you to enrich 
your content portals, e-commerce sites and other content based websites.

### Access credentials and the Sandbox

To access the Sugestio service, you need an account name and a secret key. 
To run the examples from the tutorial, you can use the following credentials:

* account name: <code>sandbox</code>
* secret key: <code>demo</code>

The Sandbox is a *read-only* account. You can use these credentials to experiment 
with the service. The Sandbox can give personal recommendations for users 1 through 5, 
and similar items for items 1 through 5.

When you are ready to work with real data, you may apply for a developer account through 
the [Sugestio website](http://www.sugestio.com).  

## About this library

### Features

The following [API](http://www.sugestio.com/documentation) features are implemented:

* get personalized recommendations for a given user
* get items that are similar to a given item
* submit and retrieve user activity (consumptions): clicks, purchases, ratings, ...
* submit and retrieve item metadata: description, location, tags, categories, ...
* submit and retrieve user metadata: gender, location, birthday, ...
* bulk submission of consumptions and item/user metadata

### Requirements

This library is compatible with Python 2.7, 3.4 and 3.6. It requires [python-oauth2](https://github.com/joestump/python-oauth2) which in turn depends on <code>httplib2</code>. Installing python-oauth2 should automatically install the http2lib2 dependency. python-oauth2 can be installed through the PIP tool:

    $ pip install oauth2
    
Or alternatively on Windows (may require an elevated command prompt):

    > python.exe -m pip install oauth2
    
The use of [virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is recommended.

# Tutorial and sample code

Get top 5 personal recommendations for user with id 1:

	import sugestio

	ACCOUNT = 'sandbox'
	SECRET = 'demo'

	client = sugestio.Client(ACCOUNT, SECRET)

	status, content = client.get_recommendations(1, 5)

    if status == 200:
        print("Title\tScore")
        for recommendation in content:
            print(recommendation.item.title + "\t" + str(recommendation.score))
    else:
        print("server response code:", status)


<code>example.py</code> contains more sample code that illustrates how you can use the library.
