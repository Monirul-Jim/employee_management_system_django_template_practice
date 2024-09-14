from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class EmployeeModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    designation = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
