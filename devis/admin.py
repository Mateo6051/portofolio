import base64
import os
from django.http import HttpResponse
from .models import Tache, Client, Devis
from django.contrib import admin
from django.conf import settings
from django.template.loader import render_to_string
import pdfkit
TVA = getattr(settings, "TVA", 0)
STATIC_ROOT = getattr(settings, "STATIC_ROOT", None)


# Register your models here.


def generate_devis_pdf(queryset, download=False):
    devis = Devis.objects.all().first()
    image_path = os.path.join( 'images', 'logo.png')
    path = os.path.join(STATIC_ROOT, image_path)
    print(path)
    with open(path, 'rb') as logo:
        encoded_logo = base64.b64encode(logo.read()).decode()
    logo.close()

    context = {
        "devis": devis,
        'tva': TVA,
        "logo": encoded_logo,
    }
    html_template = render_to_string(
        'devis.html', context)
    css_path = os.path.join('css', 'devis.css')

    css = os.path.join(STATIC_ROOT, css_path)
    print(css)
    options = {
        'page-size': 'A4',
        'page-width': '210mm',
        'page-height': '297mm',
        'enable-local-file-access': None,
        'encoding': "UTF-8",
        'margin-bottom': '15mm',
        'margin-top': '10mm',
        'margin-left': '0mm',
        'margin-right': '0mm',
        "load-error-handling": "ignore",
    }
    pdf = pdfkit.from_string(html_template,
                             False, options=options, css=css)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="devis_' + \
        devis.numero + '.pdf"'
    return response


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
