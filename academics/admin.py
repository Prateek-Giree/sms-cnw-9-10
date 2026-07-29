from django.contrib import admin
from .models import Subject, Assignment, Marks

# Register your models here.
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Marks)
