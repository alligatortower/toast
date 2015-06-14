from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from model_mommy import mommy


class SimpleTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


class TestGame(TestCase):
    def setUp(self):
        pass


class TestViews(TestCase):
    def setUp(self):
        pass

    def test_create_game_View(self):
        response = self.client.get(reverse('create_game'))
        import ipdb; ipdb.set_trace()


from djangojs.runners import JsTestCase
from djangojs.runners import QUnitSuite


class QunitTests(QUnitSuite, JsTestCase):
    title = 'Qunit tests'
    url_name = 'qunit_view'
