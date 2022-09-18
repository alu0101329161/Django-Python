from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404
from .forms import CreateNewTask, CreateNewProject
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.


def login(request):
    if (request.method == 'GET'):
        return render(request, 'login.html', {
            'form': UserCreationForm()
        })
    else:
        if (request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                # Save in database
                user.save()
                # Create a cookie for the user(session_id)
                print(user)
                login(request, user)
                return redirect(tasks)
            except IntegrityError:
                return render(request, 'login.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already taken'
                })
        else:
            return render(request, 'login.html', {
                'form': UserCreationForm(),
                'error': 'Passwords must match'
            })


def signout(request):
    logout(request)
    return redirect(index)

def signin(request):
    if (request.method == 'GET'):
        return render(request, 'login.html', {
            'form': UserCreationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': UserCreationForm(),
                'error': 'Username and password did not match'
            })
        else:
            login(request, user)
            return redirect(tasks)



def index(request):
    title = 'Welcome to my app'
    return render(request, 'index.html', {'title': title})


def about(request):
    username = 'Joseph'
    return render(request, 'about.html', {'username': username})


def hello(request, username):
    return HttpResponse('<h2> hello %s <h2>' % username)


def projects(request):
    projects = list(Project.objects.values())
    return render(request, 'projects/projects.html', {
        'projects': projects
    })


def tasks(request):
    # tasks = get_object_or_404(Task, id=id)
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })


def create_task(request):
    if request.method == 'GET':
        # show interface
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask()
        })
    else:
        Task.objects.create(
            title=request.POST['title'], description=request.POST['description'], project_id=2)
        return redirect(tasks)


def create_project(request):
    if (request.method == 'GET'):
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(name=request.POST['name'])
        return redirect(projects)


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks
    })
