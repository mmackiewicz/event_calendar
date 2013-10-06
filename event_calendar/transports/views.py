from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from tools.http import JsonResponse
from models import ReturnTransport, Transport
from vehicles.models import Vehicle
from loads.models import Load, ReturnLoad


@require_POST
def create_transport_view(request):
    load_ids = request.POST['loads_ids'].split(',')
    loads = Load.objects.filter(id__in=load_ids)
    return JsonResponse(create_transport(loads=loads, vehicle=None))

def create_transport(loads, vehicle=None):
    transport = Transport(vehicle=vehicle, loads=loads)
    transport.save()
    return transport


@require_GET
def get_transport_view(request, transport_id):
    try:
        return JsonResponse(data=Transport.objects.get(pk=transport_id))
    except Transport.DoesNotExist:
        return Http404


"""
    Return transports actions
"""

@require_POST
def create_return_transport_view(request):
    start_location = request.POST['start_location']
    end_location = request.POST['end_location']
    load_ids = request.POST['load_ids'].split(',')

    try:
        loads = ReturnLoad.objects.filter(id__in=load_ids)
        return JsonResponse(create_return_transport(start_location=start_location,
                                                    end_location=end_location,
                                                    loads=loads))
    except Vehicle.DoesNotExist:
        return Http404

def create_return_transport(start_location, end_location, loads):
    transport = ReturnTransport(start_location, end_location, loads=loads)
    transport.save()
    return transport


@require_GET
def get_return_transport_view(request, transport_id):
    try:
        return JsonResponse(data=ReturnTransport.objects.get(pk=transport_id))
    except Transport.DoesNotExist:
        return Http404