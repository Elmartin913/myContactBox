from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    description = models.TextField(null=True)

class Adress(models.Model):
    city = models.CharField(max_length=64, null=True, )
    street = models.CharField(max_length=64, null=True)
    home_number = models.IntegerField(blank=True, null=True)
    flat_number = models.IntegerField(blank=True, null=True)
    person = models.ForeignKey(Person, null=True, related_name='person')

class Phone(models.Model):
    number = models.IntegerField(blank=True, null=True)
    choices = ((1, "domowy"), (2, "służbowy"), (3, "komórkowy"))
    typ_phone = models.IntegerField(choices=choices, default=1)
    person = models.ForeignKey(Person, null=True)

class Email(models.Model):
    email = models.CharField(max_length=64, default=None)
    choices = ((1, "domowy"), (2, "służbowy"), (3, "komórkowy"))
    typ_email = models.IntegerField(choices=choices, default=1)
    person = models.ForeignKey(Person, null=True)
