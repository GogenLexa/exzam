from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.crypto import get_random_string


def get_file_name(instance, filename):
    return '/'.join([get_random_string(length=5) + '' + filename])


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='фамилия ', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='отчество', blank=True, null=True)
    password = models.CharField(max_length=254, verbose_name='пароль', blank=False)
    username = models.CharField(max_length=254, verbose_name='логин', blank=False, unique=True)
    email = models.CharField(max_length=254, verbose_name='почта', blank=False, unique=True)
    role = models.CharField(max_length=254, verbose_name='роль', blank=False,
                            choices=(('user', 'user'), ('admin', 'admin')))

    def full_name(self):
        return ''.join([self.name, self.surname, self.patronymic])

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname) + ' ' + str(self.patronymic)


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='имя', blank=False)
    country = models.CharField(max_length=254, verbose_name='старна', blank=False)
    model = models.CharField(max_length=254, verbose_name='модель', blank=False)
    date = models.DateTimeField(verbose_name='дата добавления', blank=False, auto_now_add=True)
    year = models.IntegerField(verbose_name='год создания', blank=True)
    count = models.IntegerField(verbose_name='count', default=1, blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=10, decimal_places=2, default=0.00, blank=True)
    category = models.ForeignKey('Category', verbose_name='Category', on_delete=models.CASCADE)
    photo_file = models.ImageField(verbose_name='фото продукта', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])
    ])

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='имя', blank=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    count = models.IntegerField(verbose_name='год создания', default=0, blank=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + '' + str(self.count)


class Order(models.Model):
    STATUS_CHOICES = {
        ('new', 'НОВЫЙ'), ('canceled', 'ОТМИНЕТ'), ('confirmed', 'ДА')
    }
    status = models.CharField(max_length=254, choices=STATUS_CHOICES, verbose_name='станус', default='new')
    rejection_reason = models.TextField(verbose_name='причина отказа', blank=True, null=True)
    date = models.DateTimeField(verbose_name='дата добавления', blank=False, auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='ItemInOrder', related_name='orders')

    def count_product(self):
        count = 1
        for item_order in self.iteminorder_set.all():
            count += item_order.count
        return count

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def __str__(self):
        return self.date.ctime() + '|' + self.user.full_name() + ' | ' + str(self.count_product())


class ItemInOrder(models.Model):
    count = models.IntegerField(verbose_name='год создания', default=0, blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=10, decimal_places=2, default=0.00, blank=True)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='order', on_delete=models.CASCADE)
