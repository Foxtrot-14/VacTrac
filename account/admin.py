from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name','phone','id','type','otp','is_verified', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name','type','otp')}),
        ('Permissions', {'fields': ('is_admin','is_verified')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name','type', 'otp', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone','name')
    ordering = ('phone','id','type')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)