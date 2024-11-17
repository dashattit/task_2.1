from lib2to3.fixes.fix_input import context
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from .forms import AddUserCreatingForm, AddUserLoginForm, RequestForm, RequestFilterForm
from .models import AddUser, Request
from django.views import generic
from django.views.generic.edit import FormView



class HomepageListView(generic.ListView):
    model = Request
    template_name = 'index.html'

    def get_queryset(self):
        return Request.objects.filter(status='C').order_by('-created_at')[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['design_requests_count'] = Request.objects.filter(status='P').count()
        return context

class Register(generic.CreateView):
    template_name = 'catalog/register.html'
    form_class = AddUserCreatingForm
    success_url = reverse_lazy('login')

class Login(FormView):
    template_name = 'catalog/login.html'
    form_class = AddUserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверное имя пользователя или пароль.")
            return self.form_invalid(form)  # Возвращаем форму с ошибками


class UserProfileListView(generic.ListView):
    model = Request  # или другой подходящий класс модели
    template_name = 'catalog/profile.html'
    context_object_name = 'design_requests'

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['design_requests'] = self.get_queryset()  # Передаем queryset в контекст
        context['filter_form'] = RequestFilterForm(self.request.GET or None)
        return context

def logout_user(request):
    logout(request)
    return render(request, 'catalog/logout.html')

class RequestCreateView(generic.CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'catalog/create_request.html'
    success_url = 'profile'

    def get(self, request):
        form = RequestForm()
        return render(request, 'catalog/create_request.html', {'form': form})

    def post(self, request):
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_instance = form.save(commit=False)  # Don't save yet
            request_instance.user = request.user  # Set the user field
            request_instance.save()  # Save the instance with correct category
            return redirect('profile')
        else:
            print(form.errors)  # Print out the errors for debugging
        return render(request, 'catalog/create_request.html', {'form': form})

