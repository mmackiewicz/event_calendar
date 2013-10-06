from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from tools.http import JsonResponse
from tools.auth import is_admin, is_authenticated, is_in_roles
from models import Worker
from forms import WorkerCreateForm, WorkerUpdateForm


@require_http_methods(['GET', 'POST'])
@is_admin()
def create_worker_view(request):
    if request.method == 'POST':
        form = WorkerCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            return JsonResponse(create_worker(username, password, role,))

    else:
        form = WorkerCreateForm()

    return render(request,'worker_create_form.html', {'form': form})


def create_worker(username, password, role,):
    user = User.objects.create_user(username, password=None)
    user.set_password(password)
    user.save()

    worker = Worker(role=role, user=user)
    worker.save()

    return worker.id

def update_worker(worker, username, password, role):
    worker.role = role
    worker.save()

    user = worker.get_profile()
    user.username = username
    user.set_password(password)
    user.save()

    return worker.id


@require_http_methods(['GET', 'POST'])
@is_admin()
def update_worker_view(request, worker_id):
    worker = get_object_or_404(User, pk=worker_id)

    if request.method == 'GET':
        worker_dict = {}
        worker_dict['role'] = worker.get_profile().role
        worker_dict['username'] = worker.username
        form = WorkerUpdateForm(initial=worker_dict)

    else:
        form = WorkerUpdateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['new_password1']
            role = form.cleaned_data['role']
        update_worker(worker, username, password, role)


    return render(request, 'worker_edit_form.html', {'form': form})


@require_GET
def get_worker_view(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    return JsonResponse(data=worker)

@require_GET
@is_admin()
def get_all_workers_view(request):
    workers = Worker.objects.all()
    return render(request, 'workers_list.html', {'workers': workers})

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