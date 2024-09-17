from django.db import models

# Create your models here.

class Employee(models.Model):
    DESIGNATION_CHOICES = [
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Analyst', 'Analyst'),
        ('Intern', 'Intern'),
    ]
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


