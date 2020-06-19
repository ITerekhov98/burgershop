from django.views.generic import ListView

from foodcartapp.models import OrderItem
from foodcartapp.models import User


class order_list_view(ListView):
    model = OrderItem
    template_name = "order_list.html"
    context_object_name = "orderdetails_list"

    def get_context_data(self, **kwargs):
        context = super(order_list_view, self).get_context_data(**kwargs)
        context['orders_list'] = OrderItem.objects.filter(product__restaurant__admin__user__id=self.request.user.id)
        context['Name'] = User.objects.get(id=self.request.user.id).username
        return context
