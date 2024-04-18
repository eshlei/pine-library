from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q

from .models import Book, Borrowing
from .forms import NameForm, DateTimePicker, CheckoutForm


def index(request):
	query=request.GET.get('query','')
	results = Book.objects.filter(name__contains=request.GET.get('query','')) | Book.objects.filter(summary__contains=request.GET.get('query','')) | Book.objects.filter(ISBN__contains=request.GET.get('query',''))
	return render(request, 'library/index.html', {'book_list':results, 'query':query})

class ConfirmView(PermissionRequiredMixin, generic.ListView):
	model = Borrowing
	template_name='library/confirm.html'
	permission_required = 'is_staff'

	def get_queryset(self):
		return Borrowing.objects.filter(status=1)

class CheckoutView(PermissionRequiredMixin, generic.ListView):
	model = Borrowing
	template_name='library/checkout.html'
	permission_required = 'is_staff'

	def get_queryset(self):
		return Borrowing.objects.filter(status=2)

class ReturnView(PermissionRequiredMixin, generic.ListView):
	model = Borrowing
	template_name='library/return.html'
	permission_required = 'is_staff'

	def get_queryset(self):
		return Borrowing.objects.filter(status=3)


class MybooksView(PermissionRequiredMixin, generic.ListView):
	model = Borrowing
	template_name='library/mybooks.html'
	permission_required = 'is_authenticated'

	def get_queryset(self):
		return Borrowing.objects.filter(borrower=self.request.user).exclude(status=4)







def get_name(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect(reverse('library:index'))
	else:
		form = NameForm()
	return render(request, 'library/name.html', {'form':form})

class DetailView(generic.DetailView):
	model = Book
	template_name = 'library/detail.html'

@login_required
def reserve(request, pk):
	book = get_object_or_404(Book, pk=pk)
	
	if book.borrowed == False:
		raise Http404("This book can not be reserved!")
	else:
		borrowing = Borrowing(borrower=request.user, book=book, status=1)
		borrowing.save()

	return HttpResponseRedirect(reverse('library:detail',args=(book.id,)))

@staff_member_required
def confirm_detail(request, pk):
	borrowing = get_object_or_404(Borrowing, pk=pk)
	if borrowing.status != 1:
		raise Http404("This book can not be confirmed!")

	if request.method == 'POST':
		time_string = request.POST.get('datetime',0)
		time = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
		borrowing.confirm_staff = request.user
		borrowing.status = 2
		borrowing.date_borrowed = time
		borrowing.save()
		return HttpResponseRedirect(reverse('library:confirm'))
	return render(request, 'library/confirm_detail.html', {'borrowing':borrowing, 'now':datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 'id':pk})

@staff_member_required
def checkout_detail(request, pk):
	borrowing = get_object_or_404(Borrowing, pk=pk)
	if borrowing.status != 2:
		raise Http404("This book can not be checked out!")

	if request.method == 'POST':
		if request.POST.get('check',''):
			borrowing.checkout_staff = request.user
			borrowing.status = 3
			borrowing.date_borrowed = datetime.now()
			borrowing.save()
			return HttpResponseRedirect(reverse('library:checkout'))
	return render(request, 'library/checkout_detail.html', {'borrowing':borrowing, 'id':pk})


@staff_member_required
def return_detail(request, pk):
	borrowing = get_object_or_404(Borrowing, pk=pk)
	if borrowing.status != 3:
		raise Http404("This book can not be returned!")

	if request.method == 'POST':
		if request.POST.get('check',''):
			borrowing.checkout_staff = request.user
			borrowing.status = 4
			borrowing.date_returned = datetime.now()
			borrowing.save()
			return HttpResponseRedirect(reverse('library:return'))
	return render(request, 'library/return_detail.html', {'borrowing':borrowing, 'id':pk})


@staff_member_required
def status_detail(request, pk):
	borrowing = get_object_or_404(Borrowing, pk=pk)
	if request.method == 'POST':
		borrowing.status = request.POST['status']
		borrowing.save()
		return HttpResponseRedirect(reverse('library:index'))
	return render(request, 'library/status_detail.html', {'borrowing':borrowing, 'id':pk})