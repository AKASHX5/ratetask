from django.urls import path, include
from .views import (
    PortApiView,RegionApiView,PriceApiView
)
# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('v1/ports', port_list, basename='delivery-api')



urlpatterns = [
    path('task/ports', PortApiView.as_view()),
    path('task/region', RegionApiView.as_view()),
    path('task/price', PriceApiView.as_view())

]
