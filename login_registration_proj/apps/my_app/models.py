from django.db import models
import string
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Your first name needs to be at least two characters long"
        if postData['first_name'].isalpha() == False:
            errors["first_name"] = "Your first name needs to consist of only alphabetic characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Your last name needs to be at least two characters long"
        if postData['last_name'].isalpha() == False:
            errors["last_name"] = "Your last name needs to consist of only alphabetic characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "The email address you entered is not valid"
        if User.objects.filter(email=postData['email']):
            errors['email'] = "This email address already exists in our system"
        if len(postData['password']) < 8:
            errors["password"] = "Your password needs to be at least eight characters long"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Your passwords do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="user_messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message, related_name="message_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


