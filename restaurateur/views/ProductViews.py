from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from ..forms.ProductsForms import AddProduct
from ..forms.ProductsForms import UpdateProduct
from foodcartapp.models import Product


class RestautantAdminsOnly(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.administrated_restaurants.exists()


class ProductListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("restaurateur:login")
    model = Product
    template_name = "products_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        # FIXME кто имеет права на редактирование ассортимента?
        return {
            **super().get_context_data(**kwargs),
            'products': Product.objects.all(),
        }
