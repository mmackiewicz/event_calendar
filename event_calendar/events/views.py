from django.db import transaction
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404, render_to_response
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from models import Event
from tools.http import JsonResponse
from tools.utils import validate_date
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

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def create_event_view(request):
    if request.method == 'POST':
        # read json and create event
        event = create_event_from_json(request.body)

        if event:
            return JsonResponse(data=event.id)
        else:
            return JsonResponse(data={'status': 'ERROR'})
    else:
        #prepare data for form
        date = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
        vehicles = v_models.Vehicle.objects.all()
        products = p_models.Product.objects.all()
        drivers = w_models.Worker.objects.all()
        resp_dict = {'vehicles': vehicles,
                     'products': products,
                     'drivers': drivers}
        #add date to response if it matches pattern YYYY-mm-dd
        if date and validate_date(date):
            resp_dict['date'] = date

        return render_to_response('event_create_form.html',resp_dict)

@transaction.commit_manually
def create_event_from_json(json_string):
    try:

        event_obj = json.loads(json_string)

        # create load objects
        loads = []
        for load_obj in event_obj['products']:
            load = l_models.Load.objects.create(amount=load_obj['amount'],
                                                product_id=load_obj['product_id'])
            loads.append(load)

        # create event object
        event = Event.objects.create(producer=event_obj['producer'],
                      recipient=event_obj['recipient'],
                      production_date=datetime.strptime(event_obj['production_date'], '%Y-%m-%d'),
                      recipients_date=datetime.strptime(event_obj['recipients_date'],'%Y-%m-%d'),
                      comment=event_obj['comment'])

        # add previously created load objects to event object
        for load in loads:
            event.loads.add(load.id)

        transaction.commit()
        return event

    except:
        transaction.rollback()
        return None


@require_GET
def monthly_events_view(request, year, month):
    start_date = datetime.strptime('-'.join((year,month,'01')), '%Y-%m-%d')
    end_date = (start_date + relativedelta(months=1)) + relativedelta(days=-1)

    events = Event.objects.filter(recipients_date__gte=start_date, recipients_date__lte=end_date)

    return JsonResponse(data={'events': [event.serialize_to_json() for event in list(events)]})

@require_GET
def daily_events_view(request, year, month, day):
    events_date = datetime.strptime('-'.join((year,month,day)), '%Y-%m-%d')

    events = Event.objects.filter(recipients_date=events_date)

    return render_to_response('event.html', {'events': [event.serialize_to_json() for event in events]})

@require_GET
def daily_events_view_json(request, year, month, day):
    events_date = datetime.strptime('-'.join((year,month,day)), '%Y-%m-%d')

    events = Event.objects.filter(recipients_date=events_date)

    return JsonResponse(data={'events': [event.serialize_to_json() for event in list(events)]})

@csrf_exempt
@require_POST
def set_vehicle_view(request):
    try:
        vehicle = get_object_or_404(v_models.Vehicle, pk=request.POST['vehicle_id'])
        event = get_object_or_404(Event, pk=request.POST['event_id'])

        event.vehicle = vehicle
        event.save()

        return JsonResponse(data={'status': 'OK'})
    except Http404:
        return JsonResponse(data={'status': 'Error'})

#def create_return_event_view(request, )