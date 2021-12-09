import json

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from guardian.shortcuts import get_objects_for_user

from nodeodm.models import ProcessingNode
from app.models import Project, Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django import forms
from webodm import settings

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    print("index in ")
    # Check first access
    if User.objects.filter(is_superuser=True).count() == 0:
        if settings.SINGLE_USER_MODE:
            # Automatically create a default account
            User.objects.create_superuser('admin', 'admin@localhost', 'admin')
        else:
            # the user is expected to create an admin account
            return redirect('welcome')

    if settings.SINGLE_USER_MODE and not request.user.is_authenticated:
        login(request, User.objects.get(username="admin"), 'django.contrib.auth.backends.ModelBackend')

    return redirect(settings.LOGIN_REDIRECT_URL if request.user.is_authenticated
                    else settings.LOGIN_URL)

@login_required
@csrf_exempt
def dashboard(request):
    print("dashboard in~~~~~")
    no_processingnodes = ProcessingNode.objects.count() == 0
    if no_processingnodes and settings.PROCESSING_NODES_ONBOARDING is not None:
        return redirect(settings.PROCESSING_NODES_ONBOARDING)

    no_tasks = Task.objects.filter(project__owner=request.user).count() == 0

    # Create first project automatically
    if Project.objects.count() == 0:
        Project.objects.create(owner=request.user, name=_("First Project"))

    return render(request, 'app/dashboard.html', {'title': _('Dashboard'),
        'no_processingnodes': no_processingnodes,
        'no_tasks': no_tasks
    })


@login_required
@csrf_exempt
def map(request, project_pk=None, task_pk=None):
    print("map in~~~~~")
    title = _("Map")

    if project_pk is not None:
        project = get_object_or_404(Project, pk=project_pk)
        if not request.user.has_perm('app.view_project', project):
            raise Http404()
        
        if task_pk is not None:
            task = get_object_or_404(Task.objects.defer('orthophoto_extent', 'dsm_extent', 'dtm_extent'), pk=task_pk, project=project)
            title = task.name or task.id
            mapItems = [task.get_map_items()]
        else:
            title = project.name or project.id
            mapItems = project.get_map_items()

    return render(request, 'app/map.html', {
            'title': title,
            'params': {
                'map-items': json.dumps(mapItems),
                'title': title,
                'public': 'false',
                'share-buttons': 'false' if settings.DESKTOP_MODE else 'true'
            }.items()
        })


@login_required
@csrf_exempt
def model_display(request, project_pk=None, task_pk=None):

    title = _("3D Model Display")

    if project_pk is not None:
        project = get_object_or_404(Project, pk=project_pk)
        if not request.user.has_perm('app.view_project', project):
            raise Http404()

        if task_pk is not None:
            task = get_object_or_404(Task.objects.defer('orthophoto_extent', 'dsm_extent', 'dtm_extent'), pk=task_pk, project=project)
            title = task.name or task.id
        else:
            raise Http404()

    return render(request, 'app/3d_model_display.html', {
            'title': title,
            'params': {
                'task': json.dumps(task.get_model_display_params()),
                'public': 'false',
                'share-buttons': 'false' if settings.DESKTOP_MODE else 'true'
            }.items()
        })

@csrf_exempt
def about(request):
    print("about in~~~~~")
    return render(request, 'app/about.html', {'title': _('About'), 'version': settings.VERSION})

@login_required
@csrf_exempt
def processing_node(request, processing_node_id):
    pn = get_object_or_404(ProcessingNode, pk=processing_node_id)
    if not pn.update_node_info():
        messages.add_message(request, messages.constants.WARNING, '{} seems to be offline.'.format(pn))

    return render(request, 'app/processing_node.html', 
            {
                'title': _('Processing Node'), 
                'processing_node': pn,
                'available_options_json': pn.get_available_options_json(pretty=True)
            })

class FirstUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', )
        widgets = {
            'password': forms.PasswordInput(),
        }

@csrf_exempt
def welcome(request):
    print("welcome in~~~~~")
    if User.objects.filter(is_superuser=True).count() > 0:
        return redirect('index')

    fuf = FirstUserForm()

    if request.method == 'POST':
        fuf = FirstUserForm(request.POST)
        if fuf.is_valid():
            admin_user = fuf.save(commit=False)
            admin_user.password = make_password(fuf.cleaned_data['password'])
            admin_user.is_superuser = admin_user.is_staff = True
            admin_user.save()

            # Log-in automatically 
            login(request, admin_user, 'django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')

    return render(request, 'app/welcome.html',
                  {
                      'title': _('Welcome'),
                      'firstuserform': fuf
                  })

@csrf_exempt
def handler404(request):
    return render(request, '404.html', status=404)

@csrf_exempt
def handler500(request):
    return render(request, '500.html', status=500)