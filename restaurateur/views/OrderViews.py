from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from foodcartapp.models import OrderItem


class OrderListView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = "order_items.html"
    context_object_name = "order_items"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'Name': self.request.user.username,
            'order_items': OrderItem.objects.filter(product__restaurant__admin=self.request.user),
        }
