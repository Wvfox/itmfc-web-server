from django.urls import re_path

from .views import *

urlpatterns = [
    # re_path(r'^$', views.index, name='index'),
    re_path(r'^operator$', operator_list),
    re_path(r'^operator/(?P<pk>\d+)$', operator_detail),
    re_path(r'^printer$', printer_list),
    re_path(r'^printer/(?P<pk>\d+)$', printer_detail),
    re_path(r'^workstation$', workstation_list),
    re_path(r'^workstation/(?P<pk>\d+)$', workstation_detail),
    re_path(r'^workstation/(?P<pk>\d+)/printer$', workstation_printer),
]
