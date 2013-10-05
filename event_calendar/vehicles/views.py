from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import render, render_to_response, get_object_or_404
from tools.http import JsonResponse
from tools.auth import is_in_roles
from workers.models import ROLE_ADMIN, ROLE_DISPATCHER
from models import Vehicle
from forms import VehicleForm


@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def create_vehicle_view(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle_code = form.cleaned_data['vehicle_code']
            model = form.cleaned_data['vehicle_code']
            registration = form.cleaned_data['registration']
            return JsonResponse(create_vehicle(vehicle_code=vehicle_code, model=model, registration=registration).id)
    else:
        form = VehicleForm()
    return render(request, 'vehicle_create_form.html', {'form': form})

def create_vehicle(vehicle_code, model, registration):
    vehicle = Vehicle(vehicle_code=vehicle_code, model=model, registration=registration)
    vehicle.save()
    return vehicle

@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_ADMIN, ROLE_DISPATCHER])
def update_vehicle_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle_code = form.cleaned_data['vehicle_code']
            model = form.cleaned_data['model']
            registration = form.cleaned_data['registration']
            return JsonResponse(create_vehicle(vehicle_code=vehicle_code, model=model, registration=registration).id)
    else:
        vehicle_dict = {}
        vehicle_dict['vehicle_code'] = vehicle.vehicle_code
        vehicle_dict['model'] = vehicle.model
        vehicle_dict['registration'] = vehicle.registration
        form = VehicleForm(initial=vehicle_dict)
        #populate form
    return render(request, 'vehicle_create_form.html', {'form': form})


def update_vehicle(vehicle, vehicle_code, model, registration):
    vehicle.vehicle_code = vehicle_code
    vehicle.model = model
    vehicle.registration = registration
    vehicle.save()
    return vehicle

@require_GET
def get_vehicle_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    return JsonResponse(data=vehicle)


@require_GET
def get_all_vehicles_view(request):
    return render(request, 'vehicles_list.html', {'vehicles': Vehicle.objects.all()})