from unittest import TestCase
from ..utils import format_date

class Testutils(TestCase):
    def test_date_format(self):
        date_payload = {
            "date_from":"2016-01-01",
            "date_to":"2016-01-26"

        }

        date_list = format_date(date_payload['date_from'],date_payload["date_to"])
        self.assertEqual(date_payload['date_from'],date_list[0])