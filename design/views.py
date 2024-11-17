from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from .forms import AddUserCreatingForm, AddUserLoginForm, RequestForm
from .models import AddUser, Request
from django.views import generic
from django.views.generic.edit import FormView

class HomepageView(generic.ListView):
    model = Request
    template_name = 'index.html'

    def get_queryset(self):
        Request.objects.filter(status='C').order_by('-created_at')[:4]

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
    model = AddUser
    template_name = 'catalog/profile.html'

def logout_user(request):
    logout(request)
    return render(request, 'catalog/logout.html')


# class RequestCreateView(generic.CreateView):
#     model = Request
#     form_class = RequestForm
#     template_name = 'catalog/create_request.html'
#     success_url = '/catalog/profile'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid()
#
#
# class RequestListView(generic.ListView):
#     model = Request
#     template_name = 'catalog/list_request.html'
#     context_object_name = 'design_requests'
#     success_url = '/catalog/profile'
#
#     def get_queryset(self):
#         return Request.objects.Filter(user=self.request.user)
