from django.forms import ModelForm
from Webapp.models import Ticket, Review, UserFollow


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ("user", "has_response")


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ("user", "ticket",)
