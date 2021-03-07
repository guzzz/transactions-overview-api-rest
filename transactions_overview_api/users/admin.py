from django.contrib import admin

from .models import CustomerUser


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age',)
    list_filter = ('name', 'email', 'age',)
    search_fields = ('name', 'email',)

admin.site.register(CustomerUser, CustomerUserAdmin)

