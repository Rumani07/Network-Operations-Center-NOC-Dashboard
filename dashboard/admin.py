from django.contrib import admin
from .models import Sensing

@admin.register(Sensing)
class SensingAdmin(admin.ModelAdmin):
    # This creates the columns in your table
    list_display = ('id', 'ip', 'username', 'Site_name', 'Type', 'SensorID')
    
    # This adds the search bar at the top (matches the user table search)
    search_fields = ('ip', 'username', 'Site_name', 'Type')
    
    # Optional: Adds a filter sidebar on the right side for easy sorting
    list_filter = ('Type', 'Site_name')
