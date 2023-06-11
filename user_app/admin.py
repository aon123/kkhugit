from django.contrib import admin
from .models import Users
# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'password',
        'created_at',
        'updated_at'
    )
