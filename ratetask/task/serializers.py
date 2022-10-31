from rest_framework import serializers
from .models import Prices, Ports, Regions


class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ports
        fields = ['code','name','parent_slug']


class PricetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = "__all__"
