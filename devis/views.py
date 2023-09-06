from django.shortcuts import render

from django.conf import settings    
from devis.models import Devis

# Create your views here.
TVA = getattr(settings, "TVA", 0)


def devis(request):
    devis = Devis.objects.all().first()
    context = {
        "devis": devis,
        'tva': TVA
    }
    return render(request, 'devis.html', context)
