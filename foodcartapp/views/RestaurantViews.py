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
from ..models import Customer
from ..models import Restaurant
from ..models import User
from ..models import City


class PermissionHelper(PermissionRequiredMixin):
    def has_permission(self):
        user = Restaurant.objects.values('admin__id').get(id=self.kwargs['pk'])
        user_id = user['admin__id']
        return self.request.user.id == user_id


class restaurant_list_view(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Restaurant
    template_name = "restaurant_list.html"
    permission_denied_message = "User does not have permission to view Restaurant"
    context_object_name = "restaurants"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurants'] = Restaurant.objects.filter(admin__id=self.request.user.id)
        context['Name'] = User.objects.get(id=self.request.user.id).username
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
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = AddRestaurant(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.admin = request.user
            post.save()
        return redirect("foodcartapp:RestaurantView")


class UpdateRestaurantView(LoginRequiredMixin, PermissionHelper, UpdateView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Restaurant
    permission_required = "foodcartapp.change_restaurant"
    permission_denied_message = "User does not have permission to change Restaurant"
    raise_exception = True
    form_class = UpdateRestaurant
    template_name = "update_restaurant.html"
    success_url = reverse_lazy("foodcartapp:RestaurantView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(id=self.kwargs['pk'])
        context['cities'] = City.objects.all()
        return context


class DeleteRestaurantView(LoginRequiredMixin, PermissionHelper, DeleteView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Restaurant
    template_name = "restaurant_confirm_delete.html"
    permission_required = "foodcartapp.delete_restaurant"
    permission_denied_message = "User does not have permission to delete restaurant"
    raise_exception = True
    success_url = reverse_lazy("foodcartapp:RestaurantView")
