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
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        create_worker(username, password, role,)

        workers = Worker.objects.all()
        return render(request, 'workers_list.html', {'workers': workers})

    return render(request,'worker_create_form.html', {'roles': ROLES})


def create_worker(username, password, role,):
    user = User.objects.create_user(username, password=None)
    user.set_password(password)
    user.save()

    worker = Worker(role=role, user=user)
    worker.save()

    return worker.id

def update_worker(user, username, password, role):
    worker = user.get_profile()
    worker.role = role
    worker.save()

    user.username = username
    user.set_password(password)
    user.save()

    return worker.id


@require_http_methods(['GET', 'POST'])
@is_admin()
def update_worker_view(request, worker_id):
    user = get_object_or_404(User, pk=worker_id)

    if request.method == 'GET':
        worker = user.get_profile()
        return render(request, 'worker_edit_form.html', {'user': user,
                                                         'roles': ROLES,
                                                         'worker': worker})

    else:
        username = request.POST['username']
        password1 = request.POST['new_password1']
        password2 = request.POST['new_password2']
        role = request.POST['role']
        update_worker(user, username, password1, role)

        workers = Worker.objects.all()
        return render(request, "workers_list.html", {'workers': workers})


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

"""
@require_POST
@is_admin()
@csrf_exempt
def toggle_worker_status(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker.user.is_active = not worker.user.is_active
    worker.user.save()
    return JsonResponse(data={'status': 'OK'})
"""