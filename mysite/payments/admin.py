from __future__ import unicode_literals
from django.contrib import admin
from payments.models import payment,transaction

class EventModelAdmin(admin.ModelAdmin):
    list_display = ['user_id',"email", "Amount","updated_at"]
    list_display_links = ["user_id","email"]
    list_filter = ["updated_at","email","user_id"]
    list_per_page = 10
    list_editable = []
    search_fields = ["user_id","updated_at","email"]

    class Meta:
        model = payment

class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["user_id","sender","receiver", "balance","last_updated"]
    list_display_links = ["user_id","sender","receiver"]
    list_filter = ["last_updated","sender","receiver"]
    list_per_page = 10
    list_editable = []
    search_fields = ["last_updated","sender","receiver"]

    class Meta:
        model = transaction

admin.site.register(payment,EventModelAdmin)
admin.site.register(transaction,EventModelAdmin1)