from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference','account','type','user',)
    list_filter = ('account','type','user',)
    search_fields = ('reference',)

admin.site.register(Transaction, TransactionAdmin)
