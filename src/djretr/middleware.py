# -*- coding: utf-8 -*-

import random
import string
import urllib
import urlparse

from django import http
from django.conf import settings
from django.core.urlresolvers import reverse


def make_nonce(length=10, chars=(string.letters + string.digits)):
    """Generate a random nonce (number used once)."""
    
    return ''.join(random.choice(chars) for i in xrange(length))


def add_query_param(url, param, value):
    """Add a query parameter to a URL."""
    
    split = list(urlparse.urlparse(url))
    if split[4]:
        split[4] += '&'
    split[4] += urllib.urlencode([(param, value)])
    return urlparse.urlunparse(split)


class RetracerRequestMixin(object):
    
    class __metaclass__(type):
        def __new__(mcls, name, bases, attrs):
            return dict(
                ((k, v) for k, v in attrs.items() if not k.startswith('_')))
    
    def get_location(self, default=None):
        """Retrieve the currently stashed location, or a default."""
        
        return self.session.get(self.retracer_session_key, default)
    
    def pop_location(self, default=None):
        """Retrieve and clear the currently stashed location."""
        
        if default is not None:
            return self.session.pop(self.retracer_session_key, default)
        return self.session.pop(self.retracer_session_key)
    
    def stash_location(self, location):
        """Stash a location in the current session."""
        
        self.session[self.retracer_session_key] = location
    
    def stash_referrer(self, default_location=None):
        """Stash the location"""
        if 'HTTP_REFERER' in self.META:
            self.stash_location(self.META['HTTP_REFERER'])
            return True
        elif default_location:
            self.stash_location(default_location)
            return True
        return False
    
    def unstash_location(self, nonce=False, permanent=False):
        location = self.pop_location()
        if nonce:
            location = add_query_param(location, make_nonce(), '')
        if permanent:
            return http.HttpResponsePermanentRedirect(location)
        return http.HttpResponseRedirect(location)
    
    def unstash_location_with_default(self, view_name, args=None, kwargs=None,
                                      nonce=False, permanent=False):
        if '/' in view_name:
            default = view_name
        else:
            default = reverse(view_name, args=args, kwargs=kwargs)
        
        if self.get_location() is None:
            self.stash_location(default)
        
        return self.unstash_location(nonce=nonce, permanent=permanent)


class RetracerMiddleware(object):
    
    def __init__(self):
        http.HttpRequest.retracer_session_key = getattr(
            settings, 'RETRACER_SESSION_KEY', '_location')
        
        for key, value in RetracerRequestMixin.items():
            setattr(http.HttpRequest, key, value)
