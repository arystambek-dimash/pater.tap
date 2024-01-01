from django.urls import path
from api.views import GetFlats, GetUpdateDeleteFlat

urlpatterns = [
    path('flats', GetFlats.as_view(), name="flat"),
    path('flats/<int:pk>/', GetUpdateDeleteFlat.as_view(), name='flat-detail'),
]
