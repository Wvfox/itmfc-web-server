from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes

from .serializers import *


'====== OPERATOR ======'


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def operator_list(request):
    """
    List all(GET) operators, or create(POST) a new operator.
    """
    data = request.data
    if request.method == 'GET':
        operators = Operator.objects.all()
        serializer = OperatorSerializer(operators, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = OperatorSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def operator_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a operator.
    """
    try:
        operator = Operator.objects.get(pk=pk)
        data = request.data
    except Operator.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = OperatorSerializer(operator)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = OperatorSerializer(operator, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)

    elif request.method == 'DELETE':
        operator.delete()
        return HttpResponse(status=204)


'======= PRINTER ======='


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def printer_list(request):
    """
    List all(GET) printers, or create(POST) a new printer.
    """
    data = request.data
    if request.method == 'GET':
        printers = Printer.objects.all()
        serializer = PrinterSerializer(printers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = PrinterSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def printer_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a printer.
    """
    try:
        printer = Printer.objects.get(pk=pk)
        data = request.data
    except Printer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PrinterSerializer(printer)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = PrinterSerializer(printer, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)

    elif request.method == 'DELETE':
        printer.delete()
        return HttpResponse(status=204)


'======= WORKSTATION ======='


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def workstation_list(request):
    """
    List all(GET) workstations, or create(POST) a new workstation.
    """
    data = request.data
    if request.method == 'GET':
        workstations = Workstation.objects.all()
        serializer = WorkstationSerializer(workstations, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = WorkstationSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                # Add printer to workstation
                if data.get('id_printer'):
                    current_workstation = Workstation.objects.get(pk=serializer.data['id'])
                    current_workstation.printers.add(Printer.objects.get(pk=data['id_printer']))
                    current_workstation.save()
                    return JsonResponse(WorkstationSerializer(current_workstation).data, status=201)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def workstation_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a workstation.
    """
    try:
        workstation = Workstation.objects.get(pk=pk)
        data = request.data
    except Workstation.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = WorkstationSerializer(workstation)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = WorkstationSerializer(workstation, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)

    elif request.method == 'DELETE':
        workstation.delete()
        return HttpResponse(status=204)


@api_view(['PUT', 'DELETE'])
@parser_classes([JSONParser])
def workstation_printer(request, pk: int):
    """
    Add(PUT) or remove(DELETE) printer of workstation.
    """
    try:
        workstation = Workstation.objects.get(pk=pk)
        data = request.data
    except Workstation.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        workstation.printers.add(Printer.objects.get(pk=data['id_printer']))
        workstation.save()
        return JsonResponse(WorkstationSerializer(workstation).data)

    elif request.method == 'DELETE':
        workstation.printers.remove(Printer.objects.get(pk=data['id_printer']))
        workstation.save()
        return JsonResponse(WorkstationSerializer(workstation).data)
