from rest_framework import generics
from api.serializers import FlatSerializer

from api.models import Flat


class GetFlats(generics.ListCreateAPIView):
    queryset = Flat.objects.select_related('contact').prefetch_related('photos')
    serializer_class = FlatSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('contact', 'additional_detail')  # Use prefetch_related for the foreign keys
        return qs


class GetUpdateDeleteFlat(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
