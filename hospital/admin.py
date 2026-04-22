from django.contrib import admin
from .models import Patient, Bed, QueueEntry

admin.site.register(Patient)
admin.site.register(Bed)
admin.site.register(QueueEntry)