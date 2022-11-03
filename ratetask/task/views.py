from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import status
from .models import Regions, Ports, Prices
from .utils import format_date



# Create your views here.


class RegionApiView(APIView):
    '''Returns a list of PORTS->dict from given region slug
         :param region_slug: region_slug
        :type region_slug: string
    with the region slug it retrives region name and with region it retrives ports from PORT table

    request_url:http://127.0.0.1:8000/api/v1/task/region?region_slug=uk_sub
    :returns:  [{
        "code": "IESNN",
        "name": "Shannon",
        "parent_slug_id": "north_europe_sub"
    },]
    '''

    def get(self, request):
        region_slug = self.request.query_params.get('region_slug')

        region = Regions.objects.filter(slug=region_slug).values()
        region = region[0]['parent_slug_id']

        ports = Ports.objects.filter(parent_slug=region).values()

        return Response(ports)


class PriceApiView(APIView):

    def get(self, request):
        """Takes params from the user and return a list of dictionary with date and average prices.

                :param day_from: starting day
                :type day_from: string
                :param day_to: last date of the range
                :type day_to: string
                :param orig_code: origin_code
                :type orig_code: string:
                param dest: destination_code
                :type dest: string
                param region_slug: region_slug
                :type orig_code: string
                :return: list of dictionary

            request_url:http://127.0.0.1:8000/api/v1/task/price?date_from=2016-01-01&date_to=2016-01-26&orig_code=CNCWN&dest_code=FIKTK
            :returns: [
    {
        "day": "2016-01-01",
        "average_price": "null"
    },
    {
        "day": "2016-01-02",
        "average_price": 1715.5
    },
    ]

        """

        ##collect params from user
        day_from = self.request.query_params.get('date_from')
        day_to = self.request.query_params.get('date_to')
        orig_code = self.request.query_params.get('orig_code')
        dest_code = self.request.query_params.get('dest_code')
        region = self.request.query_params.get("region_slug")

        response_data = []
        result = []
        price_list = []

        if day_to and day_from and ((orig_code and dest_code) or region):
            '''check if the params are provided'''

            if region:
                '''if region is provided rather than dest or orig code populate port_code '''

                # confusion here is that with region being provided I was able to retrive list of port_codes but cant
                # define which one to take ## as a orig_code or dest_code

                parent_slug = Regions.objects.get_parent_slug(region)
                port_code = Ports.objects.get_port_code(parent_slug)

                #chosing random port code
                orig_code = port_code[10]["code"]
                dest_code = port_code[20]["code"]

            date_list = format_date(day_from, day_to)

            if date_list is None:
                return Response({"message": "please put the dates in sequence"}, status=status.HTTP_400_BAD_REQUEST)

            else:

                for day in date_list:
                    queryset = Prices.objects.get_price(day, orig_code, dest_code)
                    result.append(queryset)

                    for data in queryset:
                        price_list.append(data['price'])  # apply list comprehesion

                    # price_list = [data['price'] for data in queryset]

                    if len(price_list) > 0:
                        avg_price = sum(price_list) / len(price_list)
                        if len(price_list) > 2:
                            response = dict(day=day, average_price=avg_price)
                            response_data.append(response)
                        else:
                            response = dict(day=day, average_price="null")
                            response_data.append(response)
                    else:
                        return Response({"message": "no price data"})
                return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "please query with all the params"}, status=status.HTTP_400_BAD_REQUEST)
