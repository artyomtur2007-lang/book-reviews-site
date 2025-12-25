from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random
from core.models import Book, Genre, Review

User = get_user_model()


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными (ТОЛЬКО КНИГИ)"

    def handle(self, *args, **kwargs):

        # ЖАНРЫ
        genre_names = [
            "Драма", "Комедия", "Фантастика", "Романтика",
            "Приключения", "Триллер", "Фэнтези", "Детектив"
        ]

        genres = []
        for name in genre_names:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)

        #КНИГИ
        books_data = [
            ("1984", "Антиутопия Джорджа Оруэлла", 1949),
            ("Мастер и Маргарита", "Роман Михаила Булгакова", 1967),
            ("Властелин колец", "Фэнтези-сага", 1954),
            ("Гарри Поттер", "Магическое фэнтези", 1997),
            ("Преступление и наказание", "Роман Ф.М. Достоевского", 1866),
            ("Метро 2033", "Постапокалипсис", 2005),
            ("Дюна", "Научная фантастика", 1965),
            ("451° по Фаренгейту", "Антиутопия Рэя Брэдбери", 1953),
            ("Пикник на обочине", "Фантастика братьев Стругацких", 1972),
            ("Три товарища", "Роман Эриха Марии Ремарка", 1936),
            ("Над пропастью во ржи", "Роман Джерома Сэлинджера", 1951),
            ("Алхимик", "Философский роман Пауло Коэльо", 1988),
            ("Вино из одуванчиков", "Лирический роман Рэя Брэдбери", 1957),
            ("Собачье сердце", "Сатирическая повесть Булгакова", 1925),
            ("Мы", "Антиутопия Евгения Замятина", 1920),
            ("Американские боги", "Мифологическое фэнтези", 2001),
            ("Темная башня", "Фэнтези-сага Стивена Кинга", 1982),
        ]

        books = []
        for title, desc, year in books_data:
            book, _ = Book.objects.get_or_create(
                title=title,
                defaults={
                    "description": desc,
                    "year": year
                }
            )
            book.genres.set(random.sample(genres, k=2))
            books.append(book)

        # ОТЗЫВЫ
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("Нет пользователей в базе"))
            return

        review_texts = [
            "Отличная книга!",
            "Очень понравилось",
            "Рекомендую к прочтению",
            "Интересный сюжет",
            "Читается на одном дыхании",
        ]

        for book in books:
            for _ in range(random.randint(5, 15)):
                Review.objects.create(
                    book=book,
                    user=random.choice(users),
                    rating=random.randint(1, 5),
                    text=random.choice(review_texts)
                )

        self.stdout.write(self.style.SUCCESS("База книг и отзывов успешно заполнена "))

