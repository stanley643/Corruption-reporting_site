from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserAuthentication(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # You may consider using Django's built-in password hashing

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Post(models.Model):
    ITEM_CHOICES = (
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('picture', 'Picture'),
        ('document', 'Document'),
    )

    title = models.CharField(max_length=100)
    item_type = models.CharField(max_length=10, choices=ITEM_CHOICES)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    description = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ChatRoom(models.Model):
    post = models.OneToOneField('Post', on_delete=models.CASCADE)
    unique_identifier = models.CharField(max_length=100, unique=True)

class Message(models.Model):
    chat_room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    user = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)