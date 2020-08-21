from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView,ListView
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin



def index(request):
    """View function for home page of site."""
# Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

# Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

# The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
# Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def mos(request):
    num_mos = 5858

    context = {
        'num_books': num_mos

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'mos.html', context=context)

def home(request):
    return render(request, 'base.html')
def other(request):
    context = {
    'k1': 'Welcome to the Second page',
    }
    return render(request, 'others.html', context)





########################################################
class BookListView(generic.ListView):
    model = Book
    paginate_by = 6
from django.db.models import Q
class SearchResultsView(ListView):
    model = Book
    template_name = 'search_results.html'
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query))
        return object_list
########################################################
class BookDetailView(generic.DetailView):
    model = Book
#########################################################
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 8
##########################################################
class AuthorDetailView(generic.DetailView):
    model = Author
#########################################################
class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10
#########################################################

class GenreDetailView(generic.DetailView):
    model = Genre
    paginate_by = 10



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 4

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
#########################################################
def contact(request):
    return render(request, 'contact.html')
#########################################################
def about(request):
    return render(request, 'about.html')
