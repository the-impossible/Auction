from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse
import uuid
from datetime import datetime
# My app imports

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):

        # creates a user with the parameters
        if email is None:
            raise ValueError('Email address is required!')

        if name is None:
            raise ValueError('Full name is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
            name=name.title().strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        # create a superuser with the above parameters

        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    name = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    phone = models.CharField(
        max_length=14, db_index=True, unique=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    picture = models.ImageField(
        default='img/user.png', upload_to='uploads/', null=True)

    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'


class Furniture(models.Model):
    furniture_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    furniture_name = models.CharField(max_length=100)
    start_price = models.FloatField()
    furniture_desc = models.TextField()
    created = models.DateTimeField(
        verbose_name='date_created', auto_now_add=True)
    start_date_and_time = models.DateTimeField(null=True)
    end_date_and_time = models.DateTimeField(null=True)
    is_sold = models.BooleanField(default=False)
    sold_price = models.FloatField(blank=True, null=True)
    sold_to = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='uploads/')

    def __str__(self):
        return self.furniture_name

    class Meta:
        db_table = 'Furniture'
        verbose_name_plural = 'Furniture'


class Bidding(models.Model):
    bid_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    furniture = models.ForeignKey(
        Furniture, on_delete=models.CASCADE, blank=True, null=True)
    bider = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    bid_price = models.FloatField()
    bid_date = models.DateTimeField(
        verbose_name='bid_date', auto_now_add=True)

    def __str__(self):
        return f"{self.bider} | {self.furniture.furniture_name }"

    class Meta:
        db_table = 'Bidding'
        verbose_name_plural = 'Bidding'
