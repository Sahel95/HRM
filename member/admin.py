from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from member.models import *

admin.site.register(Members)
admin.site.register(Membership)
admin.site.register(Team)


class UsersAdmin(admin.ModelAdmin):
    # fields =
    list_display = ('first_name', 'last_name', 'kudos', 'id')
    # search_fields = ('first_name', 'last_name', 'username')

