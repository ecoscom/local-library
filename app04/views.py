import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse

from app04.models import Book, Author, BookInstance, Genre
from app04.forms import RenewBookModelForm

# Create your views here.
@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()

    num_books_contains = Book.objects.filter(title__contains='LIVRO').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_genres' : num_genres,
        'num_books_contains' : num_books_contains,
        'num_visits' : num_visits,
    }

    return render(request, 'index.html', context=context)

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'app04/borroed_list.html'    
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='e').order_by('due_back')

class LoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'app04.can_mark_returned'
    model = BookInstance
    template_name = 'app04/borroed_list.html'
    #template_name = 'app04/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='e').order_by('due_back')
        
@permission_required('app04.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'app04/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required= 'app04.can_edit_author'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required= 'app04.can_edit_author'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required= 'app04.can_edit_author'
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'app04.can_edit_book'
    model = Book
    fields = '__all__'

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "app04.can_edit_book"
    model = Book
    fields = "__all__"

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'app04.can_edit_book'
    model = Book
    success_url = reverse_lazy('books')