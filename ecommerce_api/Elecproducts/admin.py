from django.contrib import admin
from.models import Category,Product

class categoryadmin(admin.ModelAdmin):
    list_display=('name','slug') # to display name and slug in the lst view
    prepopulated_fields = {'slug':('name',)} # autommaticall populate slug from the name field

admin.site.register(Product)
admin.site.register(Category,categoryadmin)