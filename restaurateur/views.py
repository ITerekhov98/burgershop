from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views


from foodcartapp.models import Product


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@method_decorator(user_passes_test(is_manager, login_url='restaurateur:login'), name='dispatch')
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "products"


@method_decorator(user_passes_test(is_manager, login_url='restaurateur:login'), name='dispatch')
class RestaurantListView(LoginRequiredMixin, TemplateView):
    template_name = "restaurants_list.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'restaurants': self.request.user.administrated_restaurants.all(),
        }
