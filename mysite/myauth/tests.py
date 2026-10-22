import json
from django.test import TestCase
from django.urls import reverse


class GetCookieViewTest(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('myauth:cookie_get'))
        self.assertContains(response, 'Cookie value')


class FooBaeViewTest(TestCase):
    def test_foobar_view(self):
        response = self.client.get(reverse('myauth:foo-bar'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertEqual(json.loads(response.content), {"foo": "bar", "spam": "eggs"})
        self.assertJSONEqual(response.content, {"foo": "bar", "spam": "eggs"})

