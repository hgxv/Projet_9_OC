from django.forms import CharField
from django.shortcuts import redirect, render
from django.db.models import Value
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from Webapp.forms import TicketForm
from Webapp.models import Ticket, Review

from itertools import chain

@login_required
def index(request):
    user = request.user
    if user.is_authenticated:
        print(posts)
        return render(request,
                "Webapp/index.html",)


def posts(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)

    posts = sorted(chain(reviews, tickets),
                    key=lambda post: post.time_created,
                    reverse=True)
                    
    return render(request,
            "Webapp/posts.html",
            {"posts" : posts})



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


def ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request,
                "Webapp/ticket.html",
                {"ticket": ticket})


def ticket_create(request):
    print(request.user)
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            print(ticket.image)
            ticket.save()
            return redirect("ticket-profil", ticket.id)
    
    else:
        form = TicketForm()

    return render(request,
            "Webapp/ticket_create.html",
            {"form": form},)
