from django.contrib import admin
from .models import Session, Participant


admin.site.register(Participant)
admin.site.register(Session)