from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import render, get_object_or_404
from tools.http import JsonResponse
from tools.auth import is_in_roles
from workers.models import ROLE_ADMIN, ROLE_DISPATCHER
from models import RENTAL_COLOUR, RENTAL_ID, RENTAL_REGISTRATION, Vehicle


@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def create_vehicle_view(request):
    if request.method == 'POST':
        registration = request.POST['registration']
        colour = request.POST['colour']
        create_vehicle(registration=registration, colour=colour)

        vehicles = Vehicle.objects.all()
        return render(request, 'vehicles_list.html', {'vehicles': vehicles})

    return render(request, 'vehicle_create_form.html')

def create_vehicle(registration, colour):
    vehicle = Vehicle(registration=registration, colour=colour)
    vehicle.save()
    return vehicle

@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def update_vehicle_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    if request.method == 'POST':
        registration = request.POST['registration']
        colour = request.POST['colour']
        update_vehicle(vehicle, registration=registration, colour=colour)

        vehicles = Vehicle.objects.all()
        return render(request, 'vehicles_list.html', {'vehicles': vehicles})

    return render(request, 'vehicle_create_form.html', {'vehicle': vehicle})


def update_vehicle(vehicle, registration, colour):
    vehicle.registration = registration
    vehicle.colour = colour
    vehicle.save()
    return vehicle

@require_GET
def get_vehicle_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    return JsonResponse(data=vehicle)


@require_GET
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def get_all_vehicles_view(request):
    return render(request, 'vehicles_list.html', {'vehicles': Vehicle.objects.all()})

@require_GET
def get_vehicles_list_json(request):
    return JsonResponse(data={'vehicles': [vehicle.serialize_to_json() for vehicle in Vehicle.objects.all()]})