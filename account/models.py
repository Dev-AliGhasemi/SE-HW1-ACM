from django.db import models
from person.models import Person

class Account(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=False, related_name="account")
    amount = models.IntegerField(default=0, db_index=True)
    account_id = models.IntegerField(null=False, unique=True, db_index=True)

    def __str__(self):
        return f'{self.person} - {self.amount} - {self.account_id}'