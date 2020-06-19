from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from ..models import Restaurant


class RestautantAdminsOnly(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.administrated_restaurants.exists()


class RestaurantListView(LoginRequiredMixin, ListView):
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
