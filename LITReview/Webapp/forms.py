from django.forms import ModelForm
from Webapp.models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ("user",)
