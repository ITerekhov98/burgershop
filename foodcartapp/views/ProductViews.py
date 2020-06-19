from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from foodcartapp.forms.ProductsForms import AddProduct
from foodcartapp.forms.ProductsForms import UpdateProduct
from foodcartapp.models import Restaurant
from foodcartapp.models import Product
from foodcartapp.models import User


class PermissionHelper(PermissionRequiredMixin):
    def has_permission(self):
        user = Product.objects.values('restaurant__admin__id').get(id=self.kwargs['pk'])
        user_id = user['restaurant__admin__id']
        return self.request.user.id == user_id


class product_list_view(ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "products_list"

    def get_context_data(self, **kwargs):
        context = super(product_list_view, self).get_context_data(**kwargs)
        context['products_list'] = Product.objects.filter(restaurant__admin__user__id=self.request.user.id)
        context['Name'] = User.objects.get(id=self.request.user.id).username
        return context


class AddProductView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = reverse_lazy("foodcartapp:login")
    template_name = 'add_product.html'
    form_class = AddProduct
    permission_required = "foodcartapp.add_product"
    permission_denied_message = "User does not have permission to add Product"
    raise_exception = True
    model = Product
    success_url = reverse_lazy("foodcartapp:ProductsView")

    def get_context_data(self, **kwargs):
        context = super(AddProductView, self).get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.filter(admin_id=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("foodcartapp:ProductsView")


class UpdateProductView(LoginRequiredMixin, PermissionHelper, UpdateView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Product
    permission_denied_message = "User does not have permission to change Product"
    raise_exception = True
    form_class = UpdateProduct
    template_name = "update_product.html"
    success_url = reverse_lazy("foodcartapp:ProductsView")

    def get_context_data(self, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=self.kwargs['pk'])
        context['restaurant'] = Restaurant.objects.filter(admin_id=self.request.user.id)
        return context


class DeleteProductView(LoginRequiredMixin, PermissionHelper, DeleteView):
    login_url = reverse_lazy("foodcartapp:login")
    model = Product
    template_name = "product_confirm_delete.html"
    permission_required = "foodcartapp.delete_product"
    permission_denied_message = "User does not have permission to delete product"
    raise_exception = True
    success_url = reverse_lazy("foodcartapp:ProductsView")
