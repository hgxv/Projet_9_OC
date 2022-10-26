from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from Webapp.forms import TicketForm
from Webapp.models import Ticket, Review


@login_required
def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request,
                "Webapp/index.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("registered")

    else:
        form = UserCreationForm()
        
    return render(request,
            "Registration/register.html",
            {"form": form})

def registered(request):
    return render(request,
            "Registration/registered.html",)


def ticket(request,ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request,
                "Webapp/ticket.html",
                {"ticket": ticket})


def ticket_create(request):
    if request == "POST":
        form = TicketForm(request.POST)
        form.user = request.user
        print(form)
        if form.is_valid():
            form.save()
            return redirect("ticket", form.id)
    
    else:
        form = TicketForm()

    return render(request,
            "Webapp/ticket_create.html",
            {"form": form})
