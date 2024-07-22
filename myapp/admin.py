from django.contrib import admin

# Register your models here.
from .models import BlogModel, Profile, Contact, Comment

admin.site.register(BlogModel)
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Comment)