from django.contrib import admin

# Models
from .models import Answer, Student

# Register models in django default admin panel
admin.site.register([Answer, Student])
