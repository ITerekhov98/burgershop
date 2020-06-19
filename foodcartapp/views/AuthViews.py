from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import views as auth_views

from foodcartapp.forms.AuthForms import Login


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'title': 'Login | User',
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
                if user.is_staff:
                    return redirect("foodcartapp:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'title': 'Login | User',
            'form': form
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('foodcartapp:login')
