
from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
import random, os
from django.core.exceptions import ValidationError
import hashlib
from django.conf import settings
class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evidence_file = models.FileField(upload_to='evidences/')

# Helper function to generate a random anonymous name
def generate_anonymous_name():
    adjectives = ["Clever", "Anonymous", "Invisible", "Mysterious", "Silent", "Hidden"]
    nouns = ["Reporter", "Whistleblower", "Informant", "Messenger", "Witness"]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.randint(0, 999)
    return f"{adjective}{noun}{number}"

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    # Override the username field with the phone number
    username = models.CharField(max_length=15, unique=True)
    email = models.CharField(max_length=100, unique=True, null=True)
    phone_number = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Hash the phone number before saving
        self.phone_number = hashlib.sha256(self.phone_number.encode()).hexdigest()
        super().save(*args, **kwargs)
        
    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.phone_number  # You might want to adjust this representation based on your requirements


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    anonymous_name = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.anonymous_name:
            # Generate a unique anonymous name
            self.anonymous_name = generate_anonymous_name()
            while UserProfile.objects.filter(anonymous_name=self.anonymous_name).exists():
                self.anonymous_name = generate_anonymous_name()
        super(UserProfile, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.user.username

# Signal to create/update UserProfile when User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()



# Validators for file types
def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.mp4', '.mov', '.avi', '.wmv']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg', '.gif', '.bmp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_audio_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_document_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.FileField('ImageFile', upload_to='chat_images/', blank=True, null=True, validators=[validate_image_extension])
    video = models.FileField('VideoFile', upload_to='chat_videos/', blank=True, null=True, validators=[validate_video_extension])
    document = models.FileField('DocumentFile', upload_to='chat_documents/', blank=True, null=True, validators=[validate_document_extension])
    audio = models.FileField('AudioFile', upload_to='chat_audio/', blank=True, null=True, validators=[validate_audio_extension])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
         
        # Custom validation to ensure only one file type is uploaded
        file_fields = [self.video, self.image, self.document, self.audio]
        file_count = sum(bool(field) for field in file_fields)
        if file_count > 1:
            raise ValidationError('You can only upload one type of file (video, image, document, or audio).')
        
    def save(self, *args, **kwargs):
        self.clean()  # Call the custom validation method
        super(ChatMessage, self).save(*args, **kwargs)

    def __str__(self):
        return f"Message from {self.user.username}"