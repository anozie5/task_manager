from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# owner's account model
class User(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# work model
class Job(models.Model):
    class Status(models.Choices):
        PENDING='P', 'Pending'
        IN_PROGRESS='IP', 'In Progress'
        COMPLETED='C', 'Completed'
    
    owner=models.ForeignKey(User, on_delete=models.)
    client=models.CharField(max_length=40)
    address=models.CharField(max_length=100)
    description=models.TextField()
    due_date=models.DateField()
    work_status=models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return self.client

# payment model
class Pay(models.Model):
    class Type(models.Choices):
        CHEQUE='CH', 'Written_Cheque'
        CASH='CA', 'Paid_Cash'
        TRANSFER='TR', 'Wired_Transfer'

    client_name=models.OneToOneField(Job, on_delete=models.CASCADE)
    payment_type=models.CharField(
        max_length=2,
        choices=Type.choices,
    )
    deposit_made=models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Initial Deposit')
    payment_completed=models.BooleanField(default=False, verbose_name='Paid')

    def __str__(self):
        return self.payment_type
