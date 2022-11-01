from django.contrib.auth import get_user_model
from django.db import connection
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

# from ratetask.task.models import Prices

from ..models import Prices, Regions, Ports
from ..utils import format_date
from django.urls import reverse

# from ratetask.task.models import Prices


class PriceApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.test_data = {
            "day": "2016-01-02",
            "price": 1715,
           "orig_code":"CNGGZ",
           "dest_code":"EETLL"
            }


        connection.cursor().execute('''CREATE TABLE ports (
    code text NOT NULL,
    name text NOT NULL,
    parent_slug text NOT NULL)
''')
        connection.cursor().execute('''CREATE TABLE prices (
    orig_code text NOT NULL,
    dest_code text NOT NULL,
    day date NOT NULL,
    price integer NOT NULL
)''')
        connection.cursor().execute('''
        CREATE TABLE regions (
    slug text NOT NULL,
    name text NOT NULL,
    parent_slug text
)''')

        data = {
            "day": "2016-01-02",
            "price": 1715,
           "orig_code":"CNGGZ",
           "dest_code":"EETLL"
            }

        data2 = {
            "slug": "stockholm_area",
            "name": "Stockholm",
            "parent_slug": "scandinavia",
            }

        data3 = {
            "code":"CNCWN",
            "name":"Chiwan",
            "parent_slug":"china_south_main"
        }

        region = Regions.objects.create(slug=data2['slug'], name=data2["name"])
        new_region = Regions.objects.create(slug=data2['slug'], name=data2['name'], parent_slug=region)

        #create ports
        self.orig_port = Ports.objects.create(code=data3['code'],name=data3['name'],parent_slug=new_region)
        self.dest_port = Ports.objects.create(code=data3['code'],name=data3['name'],parent_slug=new_region)
        Prices.objects.create(orig_code=self.orig_port,dest_code=self.dest_port,day=self.test_data['day'],price=self.test_data['price'])

    def test_price_model_method(self):

        """"
        """


        #not using faker for time
        data = {
            "day": "2016-01-02",
            "price": 1715,
           "orig_code":"CNGGZ",
           "dest_code":"EETLL"
            }

        data2 = {
            "slug": "stockholm_area",
            "name": "Stockholm",
            "parent_slug": "scandinavia",
            }

        data3 = {
            "code":"CNCWN",
            "name":"Chiwan",
            "parent_slug":"china_south_main"
        }

        region = Regions.objects.create(slug=data2['slug'], name=data2["name"])
        new_region = Regions.objects.create(slug=data2['slug'], name=data2['name'], parent_slug=region)

        #create ports
        orig_port = Ports.objects.create(code=data3['code'],name=data3['name'],parent_slug=new_region)
        dest_port = Ports.objects.create(code=data3['code'],name=data3['name'],parent_slug=new_region)


        #create price
        post = Prices.objects.create(day=data['day'], price=data["price"], orig_code=orig_port, dest_code=dest_port)


        price = Prices.objects.get_price(day=data['day'],orig_code=orig_port,dest_code=dest_port)
        price2 = Prices.objects.get_price(day=data['day'],orig_code=orig_port,dest_code=dest_port)
        price3 = Prices.objects.get_price(day=data['day'],orig_code=orig_port,dest_code=dest_port)

        # print(price[0])

        self.assertEqual(price[0]['orig_code_id'],data3['code'])
        self.assertEqual(price[0]['dest_code_id'],data3['code'])
        self.assertEqual(price[0]['price'],data['price'])

    def test_price_api(self):

        url = self.client.get(reverse('price'),{"date_from":'2016-01-01',"date_to":"2016-01-26","orig_code":self.orig_port,"dest_code":self.dest_port})
        response = url.json()
        # print(response)

        # self.assertEqual(self.test_data['price'],response['price'])












#
#
# class Testutils(TestCase):
#
#     def test_date_format(self):
#         test_data = {
#
#         }
#
#         date_list = format_date()
#




    # def test_get_data(self):
    #     """Test that login is required to access this endpoint"""
    #     response = self.client.get(reverse('price'))
    #
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

