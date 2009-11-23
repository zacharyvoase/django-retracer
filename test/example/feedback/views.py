# -*- coding: utf-8 -*-

import django.http

from forms import FeedbackForm


def feedback(request):
    if request.method == 'GET':
        request.stash_referrer()
        # Display the form.
        return django.http.HttpResponse()
    elif request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            # Redirect to stashed location, or index.
            return request.unstash_location_with_default('index')
        else:
            # Display the form, with errors.
            return django.http.HttpResponseBadRequest()
    return django.http.HttpResponseNotAllowed(['GET', 'POST'])
