from django.contrib import admin
from .models import User, Code, UserProfile
# Register your models here.
admin.site.register(User)
admin.site.register(Code)
admin.site.register(UserProfile)