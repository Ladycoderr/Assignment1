from django.db import models

class Person(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50, unique=True)
    Phone = models.IntegerField()
    address = models.CharField(max_length=200)
    fullname = models.CharField(max_length=50)
    pswrd = models.CharField(max_length=50)
    iddetail = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.username


class Company(models.Model):
    name = models.CharField(max_length=300)
    about = models.CharField(max_length=600)
    address = models.CharField(max_length=1000)
    email = models.CharField(max_length=50, unique=True, default="undefined")

    def __str__(self):
        return self.name
