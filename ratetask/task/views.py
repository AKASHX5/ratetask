from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.core import serializers
from datetime import timedelta, date, datetime
# from django.http.HttpRequest import request  as rq
from rest_framework import status

from rest_framework import status
from rest_framework import permissions
from .models import Regions, Ports, Prices
from .serializers import PortSerializer, RegionSerializer, PricetSerializer
from django.http import JsonResponse, HttpResponse
from .utils import format_date


import json


# Create your views here.

class PortApiView(ListAPIView):

    serializer_class = PortSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        print(f"name is {name}")
        ports = Ports.objects.filter(name=name)
        print(ports)
        return ports


class RegionApiView(APIView):

    def get(self,request):
        region_slug = self.request.query_params.get('region_slug')

        region = Regions.objects.filter(slug=region_slug).values()
        region = region[0]['parent_slug_id']

        ports = Ports.objects.filter(parent_slug=region).values()

        print(type(region))
        return Response(ports)


class PriceApiView(APIView):

    def get(self,request):
        """Takes params from the user and return a list of dictionary with date and average prices."""


        day_from = self.request.query_params.get('date_from')
        day_to = self.request.query_params.get('date_to')
        orig_code = self.request.query_params.get('orig_code')
        dest_code = self.request.query_params.get('dest_code')
        region = self.request.query_params.get("region_slug")

        print(day_to,day_from,orig_code,dest_code)
        response_data = []
        result = []
        price_list = []
        if day_to and day_from and ((orig_code and dest_code) or region):

            if region:
                parent_slug = Regions.objects.get_parent_slug(region)
                # print(parent_slug)

                port_code = Ports.objects.get_port_code(parent_slug)

                print(port_code)

            date_list = format_date(day_from, day_to)

            if date_list is None:
                return Response({"message": "please put the dates in sequence"}, status=status.HTTP_400_BAD_REQUEST)

            else:

                for day in date_list:
                    queryset = Prices.objects.get_price(day,orig_code,dest_code)
                    result.append(queryset)

                    for data in queryset:
                        price_list.append(data['price']) #apply list comprehesion

                    # price_list = [data['price'] for data in queryset]


                    if len(price_list)>0:
                        avg_price = sum(price_list) / len(price_list)
                        if len(price_list) > 2 :
                            response = dict(day=day,average_price=avg_price)
                            response_data.append(response)
                        else:
                            response = dict(day=day, average_price="null")
                            response_data.append(response)
                    else:
                        return Response({"message": "no price data"})
                return Response(response_data, status=status.HTTP_200_OK)
            # else:
            #     return Response({"message": "please put the dates in sequence"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"please query with all the params"}, status=status.HTTP_400_BAD_REQUEST)

