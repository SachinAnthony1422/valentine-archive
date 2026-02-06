from django.contrib import admin
from .models import ValentineDay

# This tells Django: "Hey, show this table in the admin panel!"
@admin.register(ValentineDay)
class ValentineDayAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_to_unlock', 'correct_answer')
    ordering = ('date_to_unlock',)