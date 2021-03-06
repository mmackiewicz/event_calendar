from django.db import transaction
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404, render
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from models import Event, ReturnEvent
from tools.auth import is_authenticated
from tools.http import JsonResponse
from tools.utils import validate_date
from loads import models as l_models
from vehicles import models as v_models
from products import models as p_models
from transports import models as t_models
from workers import models as w_models

@require_GET
@is_authenticated()
def get_event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return JsonResponse(data=event)

@csrf_exempt
@require_http_methods(['GET', 'POST'])
@is_authenticated()
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

        return render(request, 'event_create_form.html',resp_dict)

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

@csrf_exempt
@require_http_methods(['GET', 'POST'])
@is_authenticated()
def edit_event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method=='GET':
        products = p_models.Product.objects.all()
        return render(request, 'event_edit_form.html', {'event': event.serialize_to_json(),
                                                           'products': products})
    else:
        event = update_event_from_json(event, request.body)

        if event:
            return JsonResponse(data={'status': 'OK', 'event_id': event.id})
        else:
            return JsonResponse(data={'status': 'ERROR'})

@transaction.commit_manually
def update_event_from_json(event, json_string):
    try:

        event_obj = json.loads(json_string)

        # create load objects
        new_loads = []
        for load_obj in event_obj['products']:
            load = l_models.Load.objects.create(amount=load_obj['amount'],
                                                product_id=load_obj['product_id'])
            new_loads.append(load)

        # disconnect and delete loads currently assigned to the event
        loads = event.loads.all()
        for load in loads:
            load.delete()
        event.loads.clear()

        # update fields with new data
        event.producer = event_obj['producer']
        event.recipient = event_obj['recipient']
        event.production_date = datetime.strptime(event_obj['production_date'], '%Y-%m-%d')
        event.recipients_date = datetime.strptime(event_obj['recipients_date'],'%Y-%m-%d')
        event.comment=event_obj['comment']

        # add previously created load objects to event object
        for load in new_loads:
            event.loads.add(load.id)

        event.save()

        transaction.commit()
        return event

    except:
        transaction.rollback()
        return None


@require_GET
@is_authenticated()
def monthly_events_view(request, year, month):
    start_date = datetime.strptime('-'.join((year,month,'01')), '%Y-%m-%d')
    end_date = (start_date + relativedelta(months=1)) + relativedelta(days=-1)

    events = Event.objects.filter(recipients_date__gte=start_date, recipients_date__lte=end_date)

    return JsonResponse(data={'events': [event.serialize_to_json() for event in list(events)]})

@require_GET
@is_authenticated()
def monthly_return_events_view(request, year, month):
    start_date = datetime.strptime('-'.join((year,month,'01')), '%Y-%m-%d')
    end_date = (start_date + relativedelta(months=1)) + relativedelta(days=-1)

    events = ReturnEvent.objects.filter(return_date__gte=start_date, return_date__lte=end_date)

    return JsonResponse(data={'return_events': [event.serialize_to_json() for event in list(events)]})

@require_GET
@is_authenticated()
def daily_events_view_json(request, year, month, day):
    events_date = datetime.strptime('-'.join((year,month,day)), '%Y-%m-%d')

    events = Event.objects.filter(recipients_date=events_date)

    return JsonResponse(data={'events': [event.serialize_to_json() for event in list(events)]})

@require_GET
@is_authenticated()
def daily_return_events_view_json(request, year, month, day):
    events_date = datetime.strptime('-'.join((year,month,day)), '%Y-%m-%d')

    events = ReturnEvent.objects.filter(return_date=events_date)

    return JsonResponse(data={'return_events': [event.serialize_to_json() for event in list(events)]})

@csrf_exempt
@require_POST
@is_authenticated()
def set_vehicle_view(request):
    try:
        vehicle = get_object_or_404(v_models.Vehicle, pk=request.POST['vehicle_id'])
        event = get_object_or_404(Event, pk=request.POST['event_id'])

        event.vehicle = vehicle
        event.save()

        if event.return_event:
            event.return_event.vehicle = vehicle
            event.return_event.save()

        return JsonResponse(data={'status': 'OK'})
    except Http404:
        return JsonResponse(data={'status': 'Error'})

@csrf_exempt
@require_POST
@is_authenticated()
def set_event_date(request):
    event = get_object_or_404(Event, pk=request.POST['event_id'])
    new_date = datetime.strptime(request.POST['new_date'], '%Y-%m-%d')
    event.recipients_date = new_date
    event.save()
    return JsonResponse(data={'status': 'OK'})

@csrf_exempt
@require_POST
@is_authenticated()
def set_return_event_date(request):
    event = get_object_or_404(Event, pk=request.POST['event_id'])
    if event.return_event:
        new_date = datetime.strptime(request.POST['new_date'], '%Y-%m-%d')
        event.return_event.return_date = new_date
        event.return_event.save()
        return JsonResponse(data={'status': 'OK'})
    else:
        return JsonResponse(data={'status': 'ERROR', 'errors': ['No return event for event with id = '+event.id]})


@csrf_exempt
@is_authenticated()
def create_return_event_view(request):
    if request.method == 'GET':
        event_id = request.GET.get('event_id', None)
        event = get_object_or_404(Event, pk=event_id)
        return render(request, 'return_event_create_form.html', {'event': event.serialize_to_json()})
    else:
        return_event = create_return_event_from_json(request.body)

        if return_event:
            return JsonResponse(data=return_event.id)
        else:
            return JsonResponse(data={'status': 'ERROR'})


@transaction.commit_manually
def create_return_event_from_json(json_string):
    try:

        event_obj = json.loads(json_string)

        event = Event.objects.get(id=event_obj['event_id'])

        # create returnTransport objects
        return_transports = []
        for transport_obj in event_obj['transports']:
            # create load objects
            return_loads = []
            for load_obj in transport_obj['products']:
                load = l_models.ReturnLoad.objects.create(amount=load_obj['amount'],
                                                    product=load_obj['product'])
                return_loads.append(load)

            # create transport object
            return_transport = t_models.ReturnTransport.objects.create(start_location=transport_obj['from'],
                                                                       end_location=transport_obj['to'])
            # add created load objects to transport
            for load in return_loads:
                return_transport.loads.add(load)

            return_transports.append(return_transport)


        vehicle_id = None
        if event_obj['vehicle_id']:
            vehicle_id = event_obj['vehicle_id']

        # create event object
        return_event = ReturnEvent.objects.create(
                      return_date=datetime.strptime(event_obj['return_date'], '%Y-%m-%d'),
                      comment=event_obj['comment'],
                      vehicle_id=vehicle_id)

        # add previously created transport objects to event object
        for transport in return_transports:
            return_event.transports.add(transport.id)

        # attach created returnEvent to event
        event.return_event = return_event
        event.save()

        transaction.commit()
        return return_event

    except:
        transaction.rollback()
        return None


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@is_authenticated()
def edit_return_event_view(request, event_id):
    revent = get_object_or_404(ReturnEvent, pk=event_id)
    if request.method=='GET':
        return render(request, 'return_event_edit_form.html', {'event': revent.serialize_to_json()})
    else:
        revent = update_return_event_from_json(revent, request.body)
        if revent:
            return JsonResponse(data={'status': 'OK', 'event_id': revent.id})
        else:
            return JsonResponse(data={'status': 'ERROR'})

@transaction.commit_manually
def update_return_event_from_json(return_event, json_string):
    try:

        event_obj = json.loads(json_string)

        # create new returnTransport objects
        new_return_transports = []
        for transport_obj in event_obj['transports']:
            # create load objects
            return_loads = []
            for load_obj in transport_obj['products']:
                load = l_models.ReturnLoad.objects.create(amount=load_obj['amount'],
                                                    product=load_obj['product'])
                return_loads.append(load)

            # create transport object
            return_transport = t_models.ReturnTransport.objects.create(start_location=transport_obj['from'],
                                                                       end_location=transport_obj['to'])

            # add created load objects to transport
            for load in return_loads:
                return_transport.loads.add(load)

            new_return_transports.append(return_transport)


        vehicle_id = None
        if event_obj['vehicle_id']:
            vehicle_id = event_obj['vehicle_id']

        # update return event object
        return_event.return_date = datetime.strptime(event_obj['return_date'], '%Y-%m-%d')
        return_event.comment = event_obj['comment']
        return_event.vehicle_id = vehicle_id

        # disconnect and delete all previous transports and loads
        old_transports = return_event.transports.all()
        for transport in old_transports:
            loads = transport.loads.all()
            loads.delete()
            transport.loads.clear()
        old_transports.delete()

        # add previously created transport objects to event object
        for transport in new_return_transports:
            return_event.transports.add(transport.id)


        return_event.save()

        transaction.commit()
        return return_event

    except:
        transaction.rollback()
        return None

@csrf_exempt
@require_POST
@is_authenticated()
def cancel_event(request):
    event_id = request.POST['event_id']
    event = get_object_or_404(Event, pk=event_id)
    delete_event(event)
    return JsonResponse(data={'status': 'OK'})

@csrf_exempt
@require_POST
@is_authenticated()
def cancel_return_event(request):
    event_id = request.POST['event_id']
    return_event = get_object_or_404(ReturnEvent, pk=event_id)
    delete_return_event(return_event)
    return JsonResponse(data={'status': 'OK'})


def delete_event(event):
    event.loads.all().delete()
    if event.return_event:
        delete_return_event(event.return_event)
    event.delete()

def delete_return_event(return_event):
    event = return_event.event
    event.return_event = None
    event.save()
    for transport in return_event.transports.all():
        transport.loads.all().delete()
    return_event.transports.all().delete()
    return_event.delete()