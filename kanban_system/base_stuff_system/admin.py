from django.contrib import admin
from .models import Todo, ExtendedUser, Notes, Company

# Register your models here.

admin.site.register(ExtendedUser)
admin.site.register(Todo)
admin.site.register(Notes)
admin.site.register(Company)
