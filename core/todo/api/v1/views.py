from todo.models import Task
from rest_framework import viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import requests
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from persiantools.jdatetime import JalaliDateTime
import pytz

from .serializers import TaskSerializer, LocationSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import DefaultPagination
from .filters import TaskFilter


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['title', 'complete']
    search_fields = ["title", "complete"]
    ordering_fields = ["creation_date"]
    pagination_class = DefaultPagination
    filterset_class = TaskFilter


class WeatherApiView(APIView):

    serializer_class = LocationSerializer
    api_key = "71cc1c8daf531186a1eaf9bdde22f9d1"

    def getLatAndLon(self, cityName):
        try:
            latUrl = f"http://api.openweathermap.org/geo/1.0/direct?q={cityName}&appid={self.api_key}"
            responseLat = requests.get(latUrl)
            convertedResponseLat = responseLat.json()
            lat = convertedResponseLat[0]["lat"]
            lon = convertedResponseLat[0]["lon"]
        except requests.exceptions.HTTPError as err:
            print("HTTPError", err)
        except requests.exceptions.ConnectionError as err:
            print("ConnectionError", err)
        except requests.exceptions.RequestException as err:
            print("RequestException", err)
        return lat, lon

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        city_name = serializer.validated_data["city"]

        # Check if the weather data for the city is cached
        cached_weather = cache.get(f"weather_{city_name}")
        print(cached_weather)
        if cached_weather:
            # Data is found in the cache, return the cached response
            return Response(cached_weather)

        lat, lon = self.getLatAndLon(city_name)
        if lat and lon:

            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"

                response = requests.get(url)
                response = response.json()
                data = {
                    "weather": response["weather"][0]["main"],
                    "temp": response["main"]["temp"],
                    "humidity": response["main"]["humidity"],
                    "sys_sunrise": JalaliDateTime.fromtimestamp(
                        response["sys"]["sunrise"], pytz.timezone("Asia/Tehran")
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "sys_sunset": JalaliDateTime.fromtimestamp(
                        response["sys"]["sunset"], pytz.timezone("Asia/Tehran")
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                }
                cache.set(f"weather_{city_name}", data, timeout=1200)
            except requests.exceptions.RequestException:
                return Response(
                    {"error": "Could not retrieve weather data."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        else:
            return Response({"error": "Could not retrieve coordinates."}, status=500)

        return Response(data)
