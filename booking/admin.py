from django.contrib import admin

from .models import Seat, Theatre

admin.site.register([Theatre, Seat])
