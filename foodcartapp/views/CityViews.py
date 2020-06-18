from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from foodcartapp.forms.CityForms import AddCity
from foodcartapp.forms.CityForms import UpdateCity
from foodcartapp.models import City


class PermissionHelper(PermissionRequiredMixin):
    def has_permission(self):
        if self.request.user.is_superuser:
            return True
        raise PermissionDenied


class city_list_view(PermissionHelper, ListView):
    login_url = "/login/"
    permission_denied_message = "User is not Authorized"
    model = City
    template_name = "city_list.html"
    context_object_name = "city_list"


class AddCityView(LoginRequiredMixin, PermissionHelper, CreateView):
    login_url = reverse_lazy("foodcartapp:login")
    template_name = 'add_city.html'
    form_class = AddCity
    permission_denied_message = "User does not have permission to add City"
    raise_exception = True
    model = City
    success_url = reverse_lazy("foodcartapp:CitiesView")


class UpdateCityView(LoginRequiredMixin, PermissionHelper, UpdateView):
    login_url = reverse_lazy("foodcartapp:login")
    model = City
    permission_denied_message = "User does not have permission to change City"
    raise_exception = True
    form_class = UpdateCity
    template_name = "update_city.html"
    success_url = reverse_lazy("foodcartapp:CitiesView")


class DeleteCityView(LoginRequiredMixin, PermissionHelper, DeleteView):
    login_url = reverse_lazy("foodcartapp:login")
    model = City
    template_name = "city_confirm_delete.html"
    permission_required = "foodcartapp.delete_city"
    permission_denied_message = "User does not have permission to delete city"
    raise_exception = True
    success_url = reverse_lazy("foodcartapp:CitiesView")
