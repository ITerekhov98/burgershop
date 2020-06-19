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
        return {
            **super().get_context_data(**kwargs),
            'products': Product.objects.filter(restaurant__admin=self.request.user),
            'Name': self.request.user.username,
        }


class AddProductView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = reverse_lazy("restaurateur:login")
    template_name = 'add_product.html'
    form_class = AddProduct
    permission_required = "foodcartapp.add_product"
    permission_denied_message = "User does not have permission to add Product"
    raise_exception = True
    model = Product
    success_url = reverse_lazy("restaurateur:ProductsView")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'restaurants': self.request.user.administrated_restaurants.all(),
        }


class UpdateProductView(LoginRequiredMixin, RestautantAdminsOnly, UpdateView):
    login_url = reverse_lazy("restaurateur:login")
    model = Product
    permission_denied_message = "User does not have permission to change Product"
    raise_exception = True
    form_class = UpdateProduct
    template_name = "update_product.html"
    success_url = reverse_lazy("restaurateur:ProductsView")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'product': Product.objects.get(id=self.kwargs['pk']),
            'restaurants': self.request.user.administrated_restaurants.all(),
        }


class DeleteProductView(LoginRequiredMixin, RestautantAdminsOnly, DeleteView):
    login_url = reverse_lazy("restaurateur:login")
    model = Product
    template_name = "product_confirm_delete.html"
    permission_required = "foodcartapp.delete_product"
    permission_denied_message = "User does not have permission to delete product"
    raise_exception = True
    success_url = reverse_lazy("restaurateur:ProductsView")
