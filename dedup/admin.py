from django.contrib import admin
from .models import Hash, StorageStats


admin.site.register(Hash)
admin.site.register(StorageStats)
