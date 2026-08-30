from django.db import models

class Student(models.Model):
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer_name} ({self.country})"
