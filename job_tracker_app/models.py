from django.db import models
from django.db.models.fields import related
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
WEBSITE_REGEX = re.compile(r"@^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*$@i")

# MANAGERS

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 letters long"

        elif not postData['first_name'].isalpha():
            errors['first_name_alpha'] = "First name must contain letters only"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 letters long"

        elif not postData['last_name'].isalpha():
            errors['last_name_alpha'] = "Last name must contain letters only"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email address."

        email_unique_check = User.objects.filter(email=postData['email'])

        if email_unique_check:
            errors['email'] = "Please enter a unique email."

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."

        if postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Passwords did not match"

        return errors

    def register(self, postData):
        safe_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()

        return User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password = safe_password)

    def authenticate(self, email, password):
        users = User.objects.filter(email = email)
        if users:
            user = users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
        
        return False

class JobManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['company'] < 2):
            errors['company'] = "Name of company must be at least 2 characters"

        if len(postData['role'] < 2):
            errors['role'] = "Name of role must be at least 2 characters"

        if len(postData['city'] < 2):
            errors['city'] = "Name of city must be at least 2 characters"

        if len(postData['state'] < 2):
            errors['state'] = "Please enter a 2 character abbreviation for the state"

        if not WEBSITE_REGEX.match(postData['company_website']):
            errors['company_url'] = "Please enter a valid URL for the company"

        if postData['job_posting_url'] and not WEBSITE_REGEX.match(postData['job_posting_url']):
            errors['job_posting_url'] = "Please enter a valid URL for the job company"

        return errors

class CommentManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['comment']) < 1:
            errors['comment'] = "Comment can't be empty"

        return errors

# MODELS
class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 60)

    # SPACE FOR RELATIONSHIPS IF ANY
    
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Job(models.Model):
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=2)
    company_website = models.TextField()
    job_posting_url = models.TextField()
    status_choices = [
        ("1", "Applied"),
        ("2", "Heard Back"),
        ("3", "Interview Scheduled"),
        ("4", "Interviewed"),
        ("5", "Denied"),
        ("6", "Received Offer")
    ]
    status = models.CharField(max_length=50, choices=status_choices, default="1")

    # SPACE FOR RELATIONSHIPS IF ANY

    # comments > job in in Comment class

    objects = JobManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Company: {self.company}, Role: {self.role}"

class Comment(models.Model):
    content = models.TextField()

    # SPACE FOR RELATIONSHIPS 
    job = models.ForeignKey(Job, related_name="comments", on_delete=models.CASCADE)

    objects = CommentManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)