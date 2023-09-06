from django.urls import path
from . import views
urlpatterns = [
    path('', views.devis, name='devis'),

]
