from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MyUserManager

class User(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(
        max_length=50,
        verbose_name="Last Name",
    )
    username = models.CharField(
        max_length=50, verbose_name="User Name", blank=True, null=True
    )
    email = models.EmailField(verbose_name="Email", unique=True, max_length=100)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name','last_name']

    def __str__(self):
        return self.fullname
    

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def set_fullname(self, value):
        names = value.split()
        self.first_name, self.last_name = names[0], " ".join(names[1:])

    fullname = property(get_fullname, set_fullname)