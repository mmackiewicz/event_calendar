from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from tools.http import JsonResponse
from tools.auth import is_admin
from models import Worker, ROLES


@require_http_methods(['GET', 'POST'])
@is_admin()
def create_worker_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        role = request.POST['role']
        create_worker(username, password, role,)

        workers = Worker.objects.all()
        return render(request, 'workers_list.html', {'workers': workers})

    return render(request,'worker_create_form.html', {'roles': ROLES})

@csrf_exempt
@require_POST
@is_admin()
def validate_worker_create(request):
    username = request.POST['username'].strip()
    if User.objects.filter(username=username):
        return JsonResponse(data={'status': 'ERROR',
                                  'errors': ['User with username %s already exists.'%username]})
    return JsonResponse(data={'status': 'OK'})

def create_worker(username, password, role,):
    user = User.objects.create_user(username, password=None)
    user.set_password(password)
    user.save()

    worker = Worker(role=role, user=user)
    worker.save()

    return worker.id

def update_worker(user, username, role, password=None):
    worker = user.get_profile()
    worker.role = role
    worker.save()

    user.username = username
    if password:
        user.set_password(password)
    user.save()

    return worker.id


@require_http_methods(['GET', 'POST'])
@is_admin()
def update_worker_view(request, worker_id):
    user = get_object_or_404(User, pk=worker_id)

    if request.method == 'GET':
        worker = user.get_profile()
        return render(request, 'worker_edit_form.html', {'user_entity': user,
                                                         'roles': ROLES,
                                                         'worker': worker})

    else:
        username = request.POST['username'].strip()
        password1 = request.POST['new_password1']
        password2 = request.POST['new_password2']
        role = request.POST['role']
        if password1 and password2:
            update_worker(user, username, role, password1)
        else:
            update_worker(user, username, role)

        workers = Worker.objects.all()
        return render(request, "workers_list.html", {'workers': workers})

@csrf_exempt
@require_POST
@is_admin()
def validate_worker_update(request, worker_id):
    username = request.POST['username'].strip()
    users = User.objects.filter(username=username)
    if users and not users[0].id == int(worker_id):
        return JsonResponse(data={'status': 'ERROR',
                                  'errors': ['User with username %s already exists.'%username]})
    return JsonResponse(data={'status': 'OK'})

@require_GET
@is_admin()
def get_worker_view(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    return JsonResponse(data=worker)

@require_GET
@is_admin()
def get_all_workers_view(request):
    workers = Worker.objects.all()
    return render(request, 'workers_list.html', {'workers': workers})

@csrf_exempt
@require_POST
@is_admin()
def delete_worker_view(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker.delete()
    return JsonResponse(data={'status': 'OK'})
