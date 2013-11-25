from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from tools.http import JsonResponse
from tools.auth import is_in_roles
from workers.models import ROLE_ADMIN, ROLE_DISPATCHER
from models import RENTAL_COLOUR, RENTAL_ID, RENTAL_REGISTRATION, Vehicle


@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def create_vehicle_view(request):
    if request.method == 'POST':
        registration = request.POST['registration'].strip()
        colour = request.POST['colour'].strip()
        create_vehicle(registration=registration, colour=colour)

        vehicles = Vehicle.objects.all()
        return render(request, 'vehicles_list.html', {'vehicles': vehicles})

    return render(request, 'vehicle_create_form.html')

@csrf_exempt
@require_POST
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def validate_vehicle_create(request):
    errors = []
    registration = request.POST['registration'].strip()
    colour = request.POST['colour'].strip()
    if Vehicle.objects.filter(registration=registration):
        errors.append('Vehicle with registration %s already exists.'%registration)
    if Vehicle.objects.filter(colour=colour):
        errors.append('Vehicle with chosen colour already exists.')

    if errors:
        return JsonResponse(data={'status': 'ERROR',
                                  'errors': errors})
    return JsonResponse(data={'status': 'OK'})


def create_vehicle(registration, colour):
    vehicle = Vehicle(registration=registration, colour=colour)
    vehicle.save()
    return vehicle

@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def update_vehicle_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    if request.method == 'POST':
        registration = request.POST['registration'].strip()
        colour = request.POST['colour'].strip()
        update_vehicle(vehicle, registration=registration, colour=colour)

        vehicles = Vehicle.objects.all()
        return render(request, 'vehicles_list.html', {'vehicles': vehicles})

    return render(request, 'vehicle_create_form.html', {'vehicle': vehicle})

@csrf_exempt
@require_POST
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def validate_vehicle_update(request, vehicle_id):
    errors = []
    registration = request.POST['registration'].strip()
    colour = request.POST['colour'].strip()
    vehicle_reg = Vehicle.objects.filter(registration=registration)
    if vehicle_reg and not vehicle_reg[0].id == int(vehicle_id):
        errors.append('Vehicle with registration %s already exists.'%registration)

    vehicle_col = Vehicle.objects.filter(colour=colour)
    if vehicle_col and not vehicle_col[0].id == int(vehicle_id):
        errors.append('Vehicle with chosen colour already exists.')

    if errors:
        return JsonResponse(data={'status': 'ERROR',
                                  'errors': errors})
    return JsonResponse(data={'status': 'OK'})

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