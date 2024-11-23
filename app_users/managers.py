from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class MyUserManager(UserManager):
    def create_user(self, 
                    email: str,
                    first_name: str = "",
                    last_name: str = "",
                    username: str = None,
                    password: str = None) -> User:
        
        if not email:
            raise ValidationError('Users must have an email address.')
        
        if '@' not in email:
            email = f"{email}@gmail.com"
        
        email = self.normalize_email(email=email)

        if not username:
            username = email.split('@')[0]  # Extract username from the email before '@'

        user, created = self.model.objects.get_or_create(email=email, defaults={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
        })

        if created and password:
            user.set_password(password)
            user.save(using=self._db)

        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str) -> User:
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
