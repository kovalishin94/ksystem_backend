from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import DaySerializer
from .utils import human_schedule


@api_view(['POST'])
@permission_classes([])
def index(request):
    serializer = DaySerializer(data=request.data)
    if serializer.is_valid():
        response_data = human_schedule(serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
