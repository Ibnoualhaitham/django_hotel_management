from django.contrib import admin
from .models import User  


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'address', 'phone')
    list_filter = ('user_type',)
    search_fields = ('username', 'email')  
