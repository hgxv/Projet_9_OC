from django.forms import CharField
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from Webapp.forms import TicketForm
from Webapp.models import Ticket, Review, UserFollow

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
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            print(ticket.image)
            ticket.save()
            return redirect("ticket-profil", ticket.id)
    
    else:
        ticket_form = TicketForm()

    return render(request,
            "Webapp/ticket_create.html",
            {"ticket_form": ticket_form},)


def ticket_change(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            print(ticket.image)
            ticket.save()
            return redirect("ticket-profil", ticket.id)
    
    else:
        ticket_form = TicketForm(instance=ticket)

    return render(request,
                "Webapp/ticket_create.html",
                {"ticket_form": ticket_form})


def ticket_delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        ticket.delete()
        return redirect('index')

    return render(request,
                "Webapp/ticket_delete.html",
                {"ticket": ticket})


def follows(request):
    user = request.user
    follows = UserFollow.objects.all().filter(user=user.id)
    followed = UserFollow.objects.all().filter(followed_user=user.id)

    return render(request,
                "Webapp/follows.html",
                {
                    "user": user,
                    "follows": follows,
                    "followed": followed,
                })