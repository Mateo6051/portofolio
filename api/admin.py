from django.contrib import admin

from api.models import Category, Tag, Realisation, Competence, Feature, Services

# Register your models here.


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Realisation)
admin.site.register(Competence)
admin.site.register(Feature)
admin.site.register(Services)
