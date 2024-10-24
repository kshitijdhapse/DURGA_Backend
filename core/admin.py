from django.contrib import admin
from .models import FoodItem
from .models import Branch
from .models import BranchMenu
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'branch')

    fieldsets = (
        (None, {
            "fields": (
                ('username', 'branch'),('is_superuser','is_staff'),
            ),
        }),
    )
admin.site.register(User)
admin.site.register(FoodItem)
admin.site.register(Branch)
admin.site.register(BranchMenu)