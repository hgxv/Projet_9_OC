from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,
                              blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    has_response = models.BooleanField(default=False)


class Review(models.Model):
    RATING_CHOICE = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    ticket = models.ForeignKey(Ticket,
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(validators=[
                                              MinValueValidator(0),
                                              MaxValueValidator(5)
                                              ],
                                              choices=RATING_CHOICE,)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollow(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='following')

    followed_user = models.ForeignKey(User,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
