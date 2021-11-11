from django.contrib import admin
from .models import ConservationCategory, ConservationContent, BirdingCategory, BirdingContent
from django.db import models

# Register your models here.

admin.site.register(ConservationCategory)
admin.site.register(ConservationContent)
admin.site.register(BirdingCategory)
admin.site.register(BirdingContent)
