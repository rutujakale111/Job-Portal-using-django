from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'posted_by', 'created_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at')
