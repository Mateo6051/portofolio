from django.contrib import admin

# Register your models here.
from .models import Tache, Client, Devis


def generate_devis_pdf(queryset, download=False):
    print('Affichage du devis')


@admin.action(description='Afficher le devis')
def show_devis_pdf(modeladmin, request, queryset):
    return generate_devis_pdf(queryset)


class TacheInline(admin.TabularInline):
    model = Tache
    extra = 0


class TacheAdmin(admin.ModelAdmin):
    pass


class DevisAdmin(admin.ModelAdmin):
    inlines = [TacheInline]
    actions = [show_devis_pdf]


admin.site.register(Tache, TacheAdmin)
admin.site.register(Client)
admin.site.register(Devis, DevisAdmin)
