from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Twix

# Register your models here.

# Unregister your models here.
admin.site.unregister(Group)


# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on display
    fields = ["username"]
    inlines = [ProfileInline]


# Reregister user
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Twix)
# admin.site.register(Profile)
