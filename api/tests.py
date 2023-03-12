from django.test import TestCase, Client
from django.urls import reverse
from .models import Book
from .serializers import BookSerializer
from rest_framework import status

# Create your tests here.

class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test Title", authors=['John Testname', 'Jane Testname'], published_year="2000")

    def test_serialization(self):
        serializer = BookSerializer(instance=self.book)
        expected_data = {
            "id": self.book.id,
            "external_id": None,
            "title": "Test Title",
            "authors": ['John Testname', 'Jane Testname'],
            "published_year": "2000",
            "acquired": False,
            "thumbnail": None
        }
        self.assertEqual(serializer.data, expected_data)


class ImportBooksTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('import')
        self.author = 'J.K. Rowling'

    def test_import_books(self):
        data = {'author': self.author}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        # Check that books were imported
        books_count = response.data['imported']
        self.assertGreater(books_count, 0)


class BooksTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('book_list')
        self.book1 = Book.objects.create(title='Book 1', published_year='2022', acquired=True)
        self.book2 = Book.objects.create(title='Book 2', published_year='2021', acquired=False)
        self.book3 = Book.objects.create(title='Book 3', published_year='2020')

    def test_filter_books(self):
        response = self.client.get(self.url, {'from': '2021', 'acquired': 'false'})
        self.assertEqual(response.status_code, 200)

        # Check that only Book 2 is returned
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.book2.id)

    def test_default_acquired_state(self):
        self.assertFalse(self.book3.acquired)


class TestBookDetail(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title='test_book')
        self.url = reverse('book_detail', args=[self.book.id])

    def test_retrieve_book_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_book_failed(self):
        self.url = reverse('book_detail', args=["x"])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_post_book(self):
        self.url = reverse('book_list')
        data = {"external_id": "1234",
                "title": "Test Title",
                "authors": ["John Testname"],
                "published_year": "2000",
                "acquired": True,
                "thumbnail": "some_path_to_thumbnail"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["external_id"], "1234")
        self.book = Book.objects.get(external_id = "1234")
        self.assertIsNotNone(self.book)

    def test_delete_book(self):
        self.book = Book.objects.get(title="test_book")
        self.url = reverse('book_detail', args=[self.book.id])
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
