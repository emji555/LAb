from django.db import models
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
# Required for unique book instances
import uuid
from django.contrib.auth.models import User
from datetime import date
from PIL import Image
# Create your models here.

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter agenre (e.g. Science Fiction)')
    image = models.ImageField(upload_to="catalog-image", blank=True)
    class Meta:
        ordering = ["-name"]
    def get_absolute_url(self):
        """Returns the url to access a particular genre """
        return reverse('genre-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

#######################################################################
#Old class Generi
#class Genre(models.Model):
    #"""Model representing a book genre."""
    #name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    #def __str__(self):
        #"""String for representing the Model object."""
        #return self.name

#######################################################################

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbninternational.org/content/what-isbn">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    image = models.ImageField(upload_to="catalog-image")

    @property
    def summary2(self):
        summary = self.summary
        replacements = []

        keyword_models = Genre.objects.all()
        for keyword_model in keyword_models:
            keyword = keyword_model.name
            if summary.find(keyword) > -1:
                url = "/catalog/genre/{0}".format(keyword_model.id)
                a = '<a href="{0}">{1}</a>'.format(url, keyword)
                replacements.append((keyword, a))

        keyword_models = Book.objects.all()
        for keyword_model in keyword_models:
            keyword = keyword_model.title
            if summary.find(keyword) > -1:
                url = "/catalog/book/{0}".format(keyword_model.id)
                a = '<a href="{0}">{1}</a>'.format(url, keyword)
                replacements.append((keyword, a))


        for keyword, a in replacements:
            summary = summary.replace(keyword, a)
        return summary


    def __str__(self):
        """String for representing the Model object."""
        return self.title
    def get_absolute_url(self):
        #"""Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description= 'Genre'


####################################################################

class BookInstance(models.Model):
    """Model representing a specific copy of a book
    (i.e. that can be borrowed from the library)."""
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book     = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint  = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status  = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True, default='m',
        help_text='Book availability',
    )
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

############################################################

class Author(models.Model):
    """Model representing an author."""
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    image = models.ImageField(upload_to="catalog-image", default='default.jpg')

    class Meta:
        ordering = ['first_name' ,'last_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'
