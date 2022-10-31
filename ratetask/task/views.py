from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.core import serializers
from datetime import timedelta, date, datetime
from django.http import HttpResponse
from rest_framework import status

from rest_framework import status
from rest_framework import permissions
from .models import Regions, Ports, Prices
from .serializers import PortSerializer, RegionSerializer, PricetSerializer
from django.http import JsonResponse, HttpResponse

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
        """Takes params from the user and return a list of dictionary with date and average prices.

            When a rightId key is found in an event, it gets removed
            and replaced by an overlay key-value pair where the value is
            the info required to display the resolved overlay

            :param day_from: events to resolve rights ids for
            :type events: list
            :param ddb_reader: DynamoDB reader used for reading configuration
            :type ddb_reader: m2a_api_helper.Read
            :param eventer: used for sending messages to Splunk
            :type eventer: m2a_eventer.Eventer
            """
        day_from = self.request.query_params.get('date_from')
        day_to = self.request.query_params.get('date_to')
        orig_code = self.request.query_params.get('orig_code')
        dest_code = self.request.query_params.get('dest_code')
        print(day_to,day_from,orig_code,dest_code)
        if day_to and day_from and orig_code and dest_code:

            new_date_from = datetime.strptime(day_from, "%Y-%m-%d")
            new_date_to = datetime.strptime(day_to, "%Y-%m-%d")
            response_data = []
            result = []
            date_list = []
            price_list = []


            if new_date_to > new_date_from:
                for n in range(int((new_date_to - new_date_from).days) + 1):
                    dt = ( new_date_from + timedelta(n))
                    dates = dt.strftime("%Y-%m-%d")
                    date_list.append(dates)

                for day in date_list:
                    queryset = Prices.objects.filter(day=day).filter(orig_code=orig_code).filter(dest_code=dest_code).values()
                    result.append(queryset)
                    for data in queryset:
                        price_list.append(data['price'])

                    if len(price_list)>0:
                        avg_price = sum(price_list) / len(price_list)
                        if len(price_list) > 2 :
                            # print(avg_price)
                            # response[day] = avg_price
                            response = dict(day=day,price=avg_price)
                            response_data.append(response)
                        else:
                            response = dict(day=day, price="null")
                            response_data.append(response)
                    else:
                        return Response({"message":"no price data"})

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "please put the dates in sequence"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"please query with all the params"}, status=status.HTTP_400_BAD_REQUEST)

