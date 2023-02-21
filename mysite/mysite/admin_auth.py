# utils/admin_auth.py
# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib import admin


def roles(self):
    #short_name = unicode # function to get group name
    short_name = lambda x:str(x)[:10].upper() # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in self.groups.all()])
    if self.user_permissions.count(): p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'Groups'

def last(self):
  fmt = "%Y %b %d, %H:%M"
  #fmt = "%Y %b %d, %H:%M:%S"
  if self.last_login is None:
    value = self.last_login
  else:
    value = self.last_login.strftime(fmt)

  return mark_safe("<nobr>%s</nobr>" % value)
last.allow_tags = True
last.admin_order_field = 'last_login'

def adm(self):
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'

def staff(self):
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'

from django.urls import reverse
def persons(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in self.user_set.all().order_by('username')])
persons.allow_tags = True

class UserAdmin(UserAdmin):
    list_display = ['username','id','email', 'first_name', 'last_name', 'is_active', staff, adm , roles,last]
    list_filter = ['groups','id', 'is_staff', 'is_superuser', 'is_active']
    list_per_page = 10
    search_fields =['username']

class GroupAdmin(GroupAdmin):
    list_display = ['name']
    list_display_links = ['name']
    list_per_page = 10

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)