from django.contrib import admin
from .models import Beer, Tag


admin.site.register(Beer)
admin.site.register(Tag)