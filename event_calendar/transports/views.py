from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from tools.http import JsonResponse
from models import Transport
from vehicles.models import Vehicle
from workers.models import Worker
from loads.models import Load


@require_POST
def create_transport_view(request):
    vehicle_id = request.POST['vehicle_id']
    driver_id = request.POST['driver_id']
    load_ids = request.POST['loads_ids'].split(',')

    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        driver = Worker.objects.get(pk=driver_id)
        loads = Load.objects.filter(id__in=load_ids)
        return JsonResponse(create_transport(vehicle=vehicle, driver=driver, loads=loads))
    except Vehicle.DoesNotExist, Worker.DoesNotExist:
        return Http404

def create_transport(vehicle, driver, loads):
    transport = Transport(vehicle=vehicle, driver=driver, loads=loads)
    transport.save()
    return transport


@require_GET
def get_transport_view(request, transport_id):
    try:
        return JsonResponse(data=Transport.objects.get(pk=transport_id))
    except Transport.DoesNotExist:
        return Http404

"""
@require_GET
def get_all_vehicles_view(request):
    return JsonResponse(data=Vehicle.objects.all())
"""