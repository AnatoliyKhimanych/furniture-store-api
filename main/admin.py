from django.contrib import admin
from .models import Furniture

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
  list_display=("id", "name", "price", "category")
  search_fields = ("name",)
