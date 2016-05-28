from django.contrib import admin
from models import Form, FormValues, FormContents, FormResults

# Register your models here.

admin.site.register(Form)
admin.site.register(FormValues)
admin.site.register(FormContents)
admin.site.register(FormResults)
