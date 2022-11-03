from django.db import connection
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Prices, Regions, Ports
from ..utils import format_date
from django.urls import reverse
import pytest

class PriceApiTest(TestCase):
    price_payload = {
        "day": "2016-01-02",
        "price": 1715,
        "orig_code": "CNGGZ",
        "dest_code": "EETLL"
    }

    region_payload = {
        "slug": "stockholm_area",
        "name": "Stockholm",
        "parent_slug": "scandinavia",
    }

    port_payload = {
        "code": "CNCWN",
        "name": "Chiwan",
        "parent_slug": "china_south_main"
    }

    def setUp(self):
        self.client = APIClient()

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

    def test_price_model_method(self):

        """"
        """

        region = Regions.objects.create(slug=self.region_payload['slug'], name=self.region_payload["name"])
        new_region = Regions.objects.create(slug=self.region_payload['slug'], name=self.region_payload['name'], parent_slug=region)

        #create ports
        orig_port = Ports.objects.create(code=self.port_payload['code'],name=self.port_payload['name'],parent_slug=new_region)
        dest_port = Ports.objects.create(code=self.port_payload['code'],name=self.port_payload['name'],parent_slug=new_region)

        # #create price
        Prices.objects.create(day=self.price_payload['day'], price=self.price_payload["price"], orig_code=orig_port, dest_code=dest_port)


        price = Prices.objects.get_price(day=self.price_payload['day'],orig_code=orig_port,dest_code=dest_port)

        self.assertEqual(price[0]['orig_code_id'],self.port_payload['code'])
        self.assertEqual(price[0]['dest_code_id'],self.port_payload['code'])
        self.assertEqual(price[0]['price'],self.price_payload['price'])

    def test_price_api_with_orig__dest_code(self):

        response2 = self.client.get(reverse('price'),{"date_from":'2016-01-01',"date_to":"2016-01-26","orig_code":"CNCWN","dest_code":"FIKTK"})

        self.assertEqual(response2.status_code,200)

    def test_price_api_with_improper_date_sequence(self):
        response = self.client.get(reverse('price'),
                                    {"date_to": '2016-01-01', "date_from": "2016-01-26", "orig_code": "CNCWN",
                                     "dest_code": "FIKTK"})
        self.assertEqual(response.status_code,400)
    #
    def test_price_api_with_region(self):
        pass





