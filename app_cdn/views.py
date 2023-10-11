import os
import shutil

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.decorators.http import require_http_methods

from .forms import ProjectForm, ItemForm, ItemEditForm
from .models import Project, Item

@user_passes_test(lambda u: u.is_superuser)
def home(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }

    return render(request, 'cdn/home.html', context)


@user_passes_test(lambda u: u.is_superuser)
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            if name in settings.CDN_EXCLUDED_NAMES or "/" in name or Project.objects.filter(name=name).exists():
                context = {
                    'form': form,
                    'error': "Project name already exists or is reserved, '/' is not allowed",
                }
                return render(request, 'cdn/new_project.html', context)
            form.save()
            projects = Project.objects.all()
            context = {
                'projects': projects,
            }
            return render(request, 'cdn/home.html', context)
        return render(request, 'cdn/new_project.html', {'form': form})
    form = ProjectForm()
    context = {
        'form': form,
    }
    return render(request, 'cdn/new_project.html', context)


@user_passes_test(lambda u: u.is_superuser)
def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    items = Item.objects.filter(project=project)
    absolute_url = request.build_absolute_uri()
    context = {
        'absolute_url': absolute_url,
        'project': project,
        'items': items,
    }
    return render(request, 'cdn/project.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            if project.name and form.cleaned_data['name'] != project.name:
                name = form.cleaned_data['name'].strip()
                if name in settings.CDN_EXCLUDED_NAMES or Project.objects.filter(name=name).exists():
                    context = {
                        'form': form,
                        'project': project,
                        'error': 'Project name already exists  or is reserved',
                    }
                    return render(request, 'cdn/edit_project.html', context)
                shutil.move(os.path.join(settings.MEDIA_ROOT, project.name),
                            os.path.join(settings.MEDIA_ROOT, form.cleaned_data['name'].strip()))
                items = Item.objects.filter(project=project)
                for item in items:
                    item.file.name = item.file.name.replace(project.name, form.cleaned_data['name'].strip())
                    item.save()
                project.name = form.cleaned_data['name'].strip()
            project.description = form.cleaned_data['description'].strip()
            project.url = form.cleaned_data['url'].strip()
            project.github = form.cleaned_data['github'].strip()
            project.save()
            projects = Project.objects.all()
            context = {
                'projects': projects,
            }
            return render(request, 'cdn/home.html', context)
        else:
            print("form is not valid !!!!")
    form = ProjectForm(instance=project)
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'cdn/edit_project.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, project.name)):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, project.name))
    project.delete()
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'cdn/home.html', context)


@user_passes_test(lambda u: u.is_superuser)
def new_item(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            Item.objects.create(
                project=project,
                category=form.cleaned_data['category'].strip(),
                description=form.cleaned_data['description'].strip(),
                file=request.FILES['file'],
                )
            return redirect('cdn:project', project_id=project.id)
        return render(request, 'cdn/new_item.html', {'form': form})
    form = ItemForm()
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'cdn/new_item.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    project = item.project
    if request.method == 'POST':
        form = ItemEditForm(request.POST, request.FILES)
        if form.is_valid():
            # item.name = form.cleaned_data['name']
            if item.category != form.cleaned_data['category'].strip():
                if not os.path.exists(
                        os.path.join(settings.MEDIA_ROOT, project.name, form.cleaned_data['category'].strip())):
                    os.mkdir(os.path.join(settings.MEDIA_ROOT, project.name, form.cleaned_data['category'].strip()))
                shutil.move(os.path.join(settings.MEDIA_ROOT, item.file.name),
                            os.path.join(settings.MEDIA_ROOT, project.name, form.cleaned_data['category']))
                item.file.name = project.name + '/' + form.cleaned_data['category'].strip() + '/' + item.file.name.split('/')[-1]
            item.category = form.cleaned_data['category'].strip()
            item.description = form.cleaned_data['description'].strip()
            item.save()
            return redirect('cdn:project', project_id=item.project.id)
    form = ItemEditForm(instance=item)
    context = {
        'item': item,
        'form': form,
        'project': project,
    }
    return render(request, 'cdn/edit_item.html', context)


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(['POST'])
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    project = item.project
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, item.file.name)):
        os.remove(os.path.join(settings.MEDIA_ROOT, item.file.name))
    item.delete()
    return redirect('cdn:project', project_id=project.id)
