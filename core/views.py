from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .decorators import admin_required
from .forms import RegisterForm, LoginForm, RequestForm, AcceptForm
from .models import Request


def index(request):
    done = Request.objects.filter(status='done')[:4]
    in_work = Request.objects.filter(status='in_progress').count()
    return render(request, 'core/index.html', {'done': done, 'in_work': in_work})

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('profile')
        messages.error(request, 'Неверный логин или пароль')
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    requests = Request.objects.filter(author=request.user)
    status = request.GET.get('status')
    if status in ('new', 'in_progress', 'done'):
        requests = requests.filter(status=status)
    return render(request, 'core/profile.html', {
        'requests': requests,
        'status': status,
    })

@login_required
def request_create(request):
    form = RequestForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        req = form.save(commit=False)
        req.author = request.user
        req.save()
        messages.success(request, 'Заявка создана')
        return redirect('profile')
    return render(request, 'core/request_form.html', {'form': form})

@login_required
def request_delete(request, pk):
    req = Request.objects.filter(pk=pk, author=request.user).first()
    if not req:
        messages.error(request, 'Заявка не найдена')
        return redirect('profile')
    if req.status != 'new':
        messages.error(request, 'Нельзя удалить заявку в работе или выполненную')
        return redirect('profile')
    if request.method == 'POST':
        req.photo.delete(save=False)
        req.delete()
        messages.success(request, 'Заявка удалена')
        return redirect('profile')
    return render(request, 'core/request_delete.html', {'req': req})

@admin_required
def admin_dashboard(request):
    return render(request, 'core/admin/dashboard.html')

@admin_required
def admin_requests(request):
    requests = Request.objects.all()
    status = request.GET.get('status')
    if status in ('new', 'in_progress', 'done'):
        requests = requests.filter(status=status)
    return render(request, 'core/admin/requests.html', {
        'requests': requests,
        'status': status,
    })

@admin_required
def admin_request_accept(request, pk):
    req = Request.objects.filter(pk=pk).first()
    if not req:
        messages.error(request, 'Заявка не найдена')
        return redirect('admin_requests')
    if req.status != 'new':
        messages.error(request, 'Статус уже изменен')
    form = AcceptForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        req.comment = form.cleaned_data['comment']
        req.status = 'in_progress'
        req.save()
        messages.success(request, 'Статус изменен на <Принято в работу>')
        return redirect('admin_requests')
    return render(request, 'core/admin/request_accept.html', {'form': form, 'req': req})