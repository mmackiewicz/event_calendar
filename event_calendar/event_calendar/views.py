__author__ = 'Marek Mackiewicz'

from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods


from workers.models import Worker, ROLE_ADMIN, ROLE_DISPATCHER

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'GET':
        return render_to_response('login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                data = get_home_data(user)
                return render(request, 'home.html', data)
            else:
                return render_to_response('login.html', {'state': 'User is not active'})
        else:
            return render_to_response('login.html', {'state': 'Invalid username or password'})
    else:
        return render_to_response('login.html')

@csrf_exempt
@require_GET
def home_view(request):
    data = get_home_data(request.user)
    return render(request, 'home.html', data)

@require_GET
def logout_view(request):
    logout(request)
    return render_to_response('logout.html')


def get_home_data(user):
    worker = Worker.objects.get(user=user)
    if worker.role in (ROLE_ADMIN, ROLE_DISPATCHER,):
        pass
    else:
        pass

    return {'day': {'bla'},
            'week': {'bla2'},}