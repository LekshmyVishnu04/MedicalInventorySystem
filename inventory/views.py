from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Inventory
from .forms import InventoryModelForm
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logincheck(reuqest):
    if reuqest.method == 'POST':
        form = AuthenticationForm(data=reuqest.POST)
        if form.is_valid():
            user = form.get_user()
            login(reuqest, user)
            return redirect('list')
    else:
        form = AuthenticationForm()
    return render(reuqest, 'login.html', {'form': form})


@login_required(login_url='/login/')
def list(request):
    search = request.GET.get('search')
    if search:
        data = Inventory.objects.filter(
            medicinename__icontains=search, added_by=request.user)
    else:
        data = Inventory.objects.filter(
            added_by=request.user)
    paginator = Paginator(data, 2)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'user': request.user, 'page_object': page_object}
    return render(request, 'list.html', context)


@login_required(login_url='/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    context = {
        'user': request.user
    }

    return render(request, 'logout.html', context)


@login_required(login_url='/login/')
def add(request):
    medicine_count = Inventory.objects.filter(
        added_by=request.user
    ).count()

    if medicine_count >= 5:
        messages.error(
            request,
            'You can add only 5 medicines.'
        )
        return redirect('list')
    if request.method == 'POST':
        form = InventoryModelForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.added_by = request.user
            medicine.save()
        return redirect('list')
    else:
        form = InventoryModelForm
    return render(request, 'add.html', {'form': form})


@login_required(login_url='/login/')
def edit(request, id):
    data = Inventory.objects.get(pk=id)
    if request.method == 'POST':
        form = InventoryModelForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = InventoryModelForm(instance=data)
    return render(request, 'edit.html', {'form': form})


@login_required(login_url='/login/')
def delete(request, id):
    data = Inventory.objects.get(pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect('list')
    return render(request, 'delete.html', {'data': data})
