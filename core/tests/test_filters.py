from django.test import TestCase
from core.models import Book


class FilterTests(TestCase):

    def setUp(self):
        Book.objects.create(title='Harry Potter', year=2001)
        Book.objects.create(title='Lord of the Rings', year=2003)
        Book.objects.create(title='Python Basics', year=2022)

    def test_search_by_title(self):
        response = self.client.get('/books/', {'search': 'Harry'})
        self.assertContains(response, 'Harry Potter')
        self.assertNotContains(response, 'Python Basics')

    def test_filter_by_year(self):
        response = self.client.get('/books/', {'year': 2022})
        self.assertContains(response, 'Python Basics')
        self.assertNotContains(response, 'Harry Potter')