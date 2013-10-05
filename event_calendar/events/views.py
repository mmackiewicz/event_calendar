from django.db import transaction
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404, render_to_response
import json
import datetime

from models import Event, EVENT_STATUS_WAITING
from tools.http import JsonResponse
from loads import models as l_models
from vehicles import models as v_models
from vehicles import views as v_views
from products import models as p_models
from transports import models as t_models
from workers import models as w_models

@require_GET
def get_event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return JsonResponse(data=event)

@require_GET
def get_events_view(request):
    return JsonResponse(data='multiple events')

@require_GET
def get_week_events_view(request, year, week):
    year_date = datetime.datetime.strptime(year+'-01-01', '%Y-%m-%d')
    weeks_delta = datetime.timedelta(weeks=int(week)-1)
    weeks_date = year_date + weeks_delta
    weekday = weeks_date.weekday()

    #get number of weekday to move to week start
    days_delta = datetime.timedelta(days=weekday)
    #calculate date of the week start and end
    start_date = weeks_date - days_delta
    end_date = start_date + datetime.timedelta(days=7)

    events = Event.objects.filter(start_time__gte=start_date, end_time__lte=end_date)


    return JsonResponse(data={'events': [event.serialize_to_json() for event in list(events)]})

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def create_event_view(request):
    if request.method == 'POST':
        # read json and create event
        event = create_event_from_json(request.raw_post_data)


        return JsonResponse(data=event.id)
    else:
        #prepare data for form
        vehicles = v_models.Vehicle.objects.all()
        products = p_models.Product.objects.all()
        drivers = w_models.Worker.objects.all()
        return render_to_response('event_create_form.html', {'vehicles': vehicles,
                                                             'products': products,
                                                             'drivers': drivers,})

@transaction.commit_manually
def create_event_from_json(json_string):
    try:
        event_obj = json.loads(json_string)

        transports = []
        for transport_obj in event_obj['vehicles']:
            loads = []
            for load_obj in transport_obj['products']:
                load = l_models.Load.objects.create(amount=load_obj['quantity'],
                                                    product_id=load_obj['product_id'])
                loads.append(load)
            transport = t_models.Transport.objects.create(vehicle_id=transport_obj['vehicle_id'],
                                           driver_id=transport_obj['driver_id'])
            for load in loads:
                transport.loads.add(load)
            transport.save()

            transports.append(transport)

        event = Event.objects.create(status=EVENT_STATUS_WAITING,
                      start_location=event_obj['start_loc'],
                      end_location=event_obj['end_loc'],
                      start_time=event_obj['start_time'],
                      end_time=event_obj['end_time'])
        for transport in transports:
            event.transports.add(transport)

    except:
        transaction.rollback()
    else:
        transaction.commit()
        return event

    return None
