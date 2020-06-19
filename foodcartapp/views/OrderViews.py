from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from foodcartapp.models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order_list.html"
    context_object_name = "orderdetails_list"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'Name': self.request.user.username,
            'orders_list': Order.objects.filter(items__product__restaurant__admin=self.request.user),
        }
