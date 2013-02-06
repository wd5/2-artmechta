# -*- coding: utf-8 -*-
import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, UserManager
from apps.products.models import Product

class CustomUserManager(UserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given username, e-mail and password.
        """
        now = datetime.datetime.now()

        # Normalize the address by lowercasing the domain part of the email
        # address.
        if email:
            try:
                email_name, domain_part = email.strip().split('@', 1)
            except ValueError:
                pass
            else:
                email = '@'.join([email_name, domain_part.lower()])
        else:
            email = ''

        user = self.model(username=username, email=email, is_staff=False,
                         is_active=True, is_superuser=False, last_login=now,
                         date_joined=now)

        user.set_password(password)
        user.save(using=self._db)
        return user

sex_choices = (
    (u'male', u'Мужской'),
    (u'female', u'Женский'),
)

class CustomUser(User):
    """User with app settings."""
    third_name = models.CharField(max_length=20, verbose_name=u'отчество', blank=True)
    phone = models.CharField(max_length=20, verbose_name=u'телефон', blank=True)
    fav_products = models.ManyToManyField(Product, verbose_name=u'Избранные товары', blank=True, null=True)

    # Use UserManager to get the create_user method, etc.
    objects = CustomUserManager()

    class Meta:
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'

    def get_orders(self):
        return self.order_set.all()

    def get_fav_products(self):
        return self.fav_products.published()

    def get_name(self):
        if self.last_name or self.first_name or self.third_name:
            if self.third_name:
                return '%s %s %s' % (self.last_name, self.first_name, self.third_name)
            else:
                return '%s %s' % (self.last_name, self.first_name)
        else:
            return u''