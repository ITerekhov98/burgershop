from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from ..forms.RestaurantForms import AddRestaurant
from ..forms.RestaurantForms import UpdateRestaurant
from ..models import Restaurant
from ..models import City


class RestautantAdminsOnly(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.administrated_restaurants.exists()


class restaurant_list_view(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Restaurant
    template_name = "restaurant_list.html"
    permission_denied_message = "User does not have permission to view Restaurant"
    context_object_name = "restaurants"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'restaurants': self.request.user.administrated_restaurants.all(),
            'Name': self.request.user.username,
        }

        context = super().get_context_data(**kwargs)
        return context


class AddRestaurantView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("foodcartapp:login")
    template_name = 'add_restaurant.html'
    form_class = AddRestaurant
    permission_denied_message = "User does not have permission to add Restaurant"
    raise_exception = True
    model = Restaurant
    success_url = reverse_lazy("foodcartapp:RestaurantView")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'cities': City.objects.all(),
        }

    def post(self, request, *args, **kwargs):
        form = AddRestaurant(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.admin = request.user
            post.save()
        return redirect("foodcartapp:RestaurantView")


class UpdateRestaurantView(LoginRequiredMixin, RestautantAdminsOnly, UpdateView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Restaurant
    permission_required = "foodcartapp.change_restaurant"
    permission_denied_message = "User does not have permission to change Restaurant"
    raise_exception = True
    form_class = UpdateRestaurant
    template_name = "update_restaurant.html"
    success_url = reverse_lazy("foodcartapp:RestaurantView")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'restaurant': Restaurant.objects.get(id=self.kwargs['pk']),
            'cities': City.objects.all(),
        }


class DeleteRestaurantView(LoginRequiredMixin, RestautantAdminsOnly, DeleteView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Restaurant
    template_name = "restaurant_confirm_delete.html"
    permission_required = "foodcartapp.delete_restaurant"
    permission_denied_message = "User does not have permission to delete restaurant"
    raise_exception = True
    success_url = reverse_lazy("foodcartapp:RestaurantView")
