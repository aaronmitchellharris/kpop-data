from django.contrib import admin

from .models import Group, Video
from .forms import VidForm

admin.site.register(Group)
admin.site.register(Video)

