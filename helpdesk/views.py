from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes

from .serializers import *


'====== APPLICATION ======'


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def application_list(request):
    """
    List all(GET) application, or create(POST) a new application.
    """
    data = request.data
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = ApplicationSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def application_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a application.
    """
    try:
        application = Application.objects.get(pk=pk)
        data = request.data
    except Application.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicationSerializer(application, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)

    elif request.method == 'DELETE':
        application.delete()
        return HttpResponse(status=204)

