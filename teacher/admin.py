from django.contrib import admin

# Models
from .models import Practice, Video

# Register models in django default admin panel
admin.site.register([Practice, Video])
