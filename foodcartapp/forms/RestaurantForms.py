from django.forms import ModelForm
from foodcartapp.models import Restaurant


class AddRestaurant(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['admin']


class UpdateRestaurant(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['admin']
