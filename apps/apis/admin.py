from django.contrib import admin
from django.apps import apps

# Register your models here.
app = apps.get_app_config('apis')

# admin.autodiscover_modules('apis', register_to=admin.site)
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except:
        pass