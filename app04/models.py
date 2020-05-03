from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Entre com o gênero')

    def __str__(self):
        return self.name

    objects = models.Manager()
    

from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Entre com um resumo do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre= models.ManyToManyField(Genre, help_text='Selecione o gênero do livro')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    class Meta:
        permissions = (("can_edit_book", "Create, edit and delete Book"),)

    display_genre.short_description = 'Genre'

    objects = models.Manager()

import uuid

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=False, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponível'),
        ('r', 'Reservado',)
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Status do livro',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    objects = models.Manager()


class Author(models.Model):
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_edit_author", "Edit, update and delete Author"),)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
    objects = models.Manager()

class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Linguagem do livro')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']