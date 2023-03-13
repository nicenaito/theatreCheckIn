from theatreCheckIn.models import CheckIns, Movies
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import CheckinsSerializer, MoviesSerializer

class CheckinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows checkin to be viewed or edited.
    """
    queryset = CheckIns.objects.all()
    serializer_class = CheckinsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows checkin to be viewed or edited.
    """
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer
    permission_classes = [permissions.IsAuthenticated]