# -*- coding: utf-8 -*-

import datetime

from django.db import models


class Feedback(models.Model):
    
    name = models.CharField(max_length=50)
    text = models.TextField(blank=False)
    created_at = models.DateTimeField(default=datetime.datetime.utcnow, editable=False)
