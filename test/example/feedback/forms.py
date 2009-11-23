# -*- coding: utf-8 -*-

import django.forms

from models import Feedback


class FeedbackForm(django.forms.ModelForm):
    
    class Meta:
        model = Feedback
