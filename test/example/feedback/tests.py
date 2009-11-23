# -*- coding: utf-8 -*-

__test__ = {"doctest": """

Initialize the client object.

    >>> from django.test import Client
    >>> client = Client()

I start out at the index:

    >>> client.get('/').status_code
    200

Assume I'm now on '/somepage/', and I want to submit some feedback:

    >>> client.get('/feedback/', HTTP_REFERER='/somepage/').status_code
    200

I have to submit a feedback request:

    >>> response = client.post('/feedback/', data={
    ...     'name': 'Zachary Voase',
    ...     'text': 'Awesome site!',
    ... })

This should be a temporary redirect back to '/somepage/' (although it will have
been made absolute by Django):

    >>> response.status_code, response['Location']
    (302, 'http://testserver/somepage/')

"""}

