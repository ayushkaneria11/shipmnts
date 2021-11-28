from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# APIs to be developed

# Authentication system to get Authtoken to make API calls
# API to post, update and show a question
# A question should have
# Title
# Body
# Relevant tags to the question to make it more searchable
# API to post answers to a particular question
# API to show questions and related answers
# API to accept the answer to a question
# API to upvote or downvote a question and answer
# API to get all questions related to a tag
# API to get all questions posted by a particular user



class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    has_accepted_answer = models.BooleanField(default=False)
    # answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True)

class Answer(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# class User(models.Model):
#     username = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)