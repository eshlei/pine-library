import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Book(models.Model):
	name = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	ISBN = models.IntegerField(default=0)
	date_published = models.DateField('date published', null=True)

	summary = models.TextField()

	image = models.ImageField(upload_to='photos/', default='default.png')

	def __str__(self):
		return self.name

	def borrowed(self):
		if self.borrowing_set.all().exclude(status=4):
			return True
		return False
	def status(self):
		return self.borrowing_set.all().exclude(status=4).first().status

class Borrowing(models.Model):
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='borrowed_book')

	book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

	status = models.IntegerField(default=0)

	date_borrowed = models.DateTimeField('date borrowed', null=True)
	date_returned = models.DateTimeField('date returned', null=True)

	confirm_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='confirmed_borrowing')
	checkout_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='checkouted_borrowing')
	return_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='returned_borrowing')

	def __str__(self):
		return f'b{self.id} {self.borrower} {self.book.name}'

	def due_day(self):
		return self.date_borrowed + datetime.timedelta(days=30)