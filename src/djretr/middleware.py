# -*- coding: utf-8 -*-

from django import http
from django.conf import settings
from django.core.urlresolvers import reverse


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
    
    def unstash_location(self, permanent=False):
        location = self.pop_location()
        if permanent:
            return http.HttpResponsePermanentRedirect(location)
        return http.HttpResponseRedirect(location)
    
    def unstash_location_with_default(self, view_name, permanent=False, *args, **kwargs):
        if view_name.startswith('/'):
            default = view_name
        else:
            default = reverse(view_name, args=args, kwargs=kwargs)
        
        location = self.pop_location(default=default)
        if permanent:
            return http.HttpResponsePermanentRedirect(location)
        return http.HttpResponseRedirect(location)


class RetracerMiddleware(object):
    
    def __init__(self):
        http.HttpRequest.retracer_session_key = getattr(
            settings, 'RETRACER_SESSION_KEY', '_location')
        
        for key, value in RetracerRequestMixin.items():
            setattr(http.HttpRequest, key, value)
