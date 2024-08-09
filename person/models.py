from django.core.validators import MinLengthValidator
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    national_code = models.CharField(max_length=10,
                                     null=False,
                                     unique=True,
                                     validators=[MinLengthValidator(10)])

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.national_code}'