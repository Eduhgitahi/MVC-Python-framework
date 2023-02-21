# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from freelance.models import Document,Writer
 
 
class EventModelAdmin(admin.ModelAdmin):
    list_display = ["Title", 'user_id',"writer_email", "Number_of_pages", "cost","created_at","order_number","urlhash","attachment","due_date","Accepted_status"]
    list_display_links = ["Title","user_id"]
    list_filter = ["created_at","writer_email","order_number","urlhash","user_id"]
    list_per_page = 8
    list_editable = []
    search_fields = ["Title","created_at","writer_email","order_number","urlhash"]

    class Meta:
        model = Document

class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["Title", "Number_of_pages","client_email","user_id","status","attachment","created_at"]
    list_display_links = ["Title","user_id"]
    list_filter = ["Title","client_email","user_id","created_at"]
    list_per_page = 8
    list_editable = []
    search_fields = ["Title","status","client_email", "created_at"]

    class Meta:
        model = Writer
        
admin.site.register(Document,EventModelAdmin)
admin.site.register(Writer,EventModelAdmin1)
