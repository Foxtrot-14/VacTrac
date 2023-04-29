from django.contrib import admin
from .models import Child, Due, Taken
# Register your models here.
admin.site.register(Child)
admin.site.register(Taken)
admin.site.register(Due)