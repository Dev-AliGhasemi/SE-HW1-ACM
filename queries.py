from account.models import Account
from person.models import Person
from django.db.models import Max, F, BigIntegerField, Q, Sum
from django.db import transaction
from random import *
from django.db.models.functions import Cast
import time

def q0():
    person1 = Person()
    person1.first_name = "Ali"
    person1.last_name = "Ghasemi"
    person1.national_code = 1234567890

    person2 = Person()
    person2.first_name = "Reza"
    person2.last_name = "Kazemi"
    person2.national_code = 9876543210

    person1.save()
    person2.save()
def q1():
    accounts = []

    q = Person.objects.all()

    for i in range(1, 20_000):
        if i % 2 == 0:
            accounts.append(Account(person=q[0], amount=randint(0, 1_000_000), account_id=randint(0, 2_000_000)))
        else:
            accounts.append(Account(person=q[1], amount=randint(0, 1_000_000), account_id=randint(0, 2_000_000)))

    Account.objects.bulk_create(accounts,batch_size=1000, ignore_conflicts=True)
    print("20_000 accounts created")

def q2():
    print(Account.objects.all().values('person__first_name', 'person__last_name', 'amount'))

def q3():
    print(Account.objects.all().aggregate(max_amount=Max('amount')))

def q4():
    max_amount = Account.objects.aggregate(amount=Max('amount'))['amount']
    print(Account.objects.filter(amount=max_amount))

def q5():
    print(Account.objects.all().order_by('amount')[0:5])

@transaction.atomic()
def q6(amount=2000, afrom=0, to=0):
    if afrom == to:
        raise Exception("Can not transfer to save account")
    elif amount < 0:
        raise Exception("Can not transfer negative amount")
    else:
        from_account = Account.objects.filter(id=afrom)
        to_account = Account.objects.filter(id=to)
        if from_account.exists() and to_account.exists() and (from_account[0].amount >= amount):
            from_account[0].amount -= amount
            to_account[0].amount += amount
            from_account[0].save()
            to_account[0].save()
            print("Transfer was successful.")
        else:
            raise Exception("Can not transfer fro some reason")

def q7():
    print(Account.objects.filter(account_id__gt=F('amount')))

def q8():
    print(Account.objects.filter(person__national_code__gt=F('amount')))

def q9():
    print(Account.objects.annotate(
        national_code_as_int=Cast('person__national_code', output_field=BigIntegerField())
    ).filter(national_code_as_int__gt=F('amount')))

def q10():
    accounts = []

    q = Person.objects.all()

    for i in range(1, 1_000_000):
        if i % 2 == 0:
            accounts.append(Account(person=q[0], amount=randint(0, 10_000_000), account_id=randint(0, 2_000_000)))
        else:
            accounts.append(Account(person=q[1], amount=randint(0, 10_000_000), account_id=randint(0, 2_000_000)))

    print(len(accounts))
    Account.objects.bulk_create(accounts, batch_size=10000, ignore_conflicts=True)
    print("1_000_000 accounts created")

def q10_time():
    pre_time = time.time_ns()
    accounts_q = Account.objects.filter(Q(amount__gt=2_000_000) | Q(amount__lt=1_000_000))
    post_time = time.time_ns()
    print(post_time - pre_time)

def q11():
    print(Person.objects.annotate(total_amount=Sum('account__amount')).values('first_name','last_name','total_amount'))
