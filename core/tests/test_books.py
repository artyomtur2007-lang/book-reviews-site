from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Book, Review

User = get_user_model()


class BookCrudTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='pass123'
        )

        self.book = Book.objects.create(
            title='Test Book',
            year=2024,
            description='Test description'
        )

    def test_create_book(self):
        self.assertEqual(Book.objects.count(), 1)

    def test_add_review(self):
        review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=5,
            text='Отличная книга'
        )

        self.book.refresh_from_db()
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(self.book.average_rating, 5.0)

    def test_delete_review(self):
        review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=4,
            text='Хорошо'
        )

        review.delete()
        self.book.refresh_from_db()

        self.assertEqual(Review.objects.count(), 0)
        self.assertEqual(self.book.average_rating, 0.0)