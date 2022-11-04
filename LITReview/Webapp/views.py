from django.forms import CharField
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from Webapp.forms import TicketForm, ReviewForm
from Webapp.models import Ticket, Review, UserFollow
from django.db.models import CharField, Value

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
    tickets = Ticket.objects.filter(user=user).annotate(type=Value('TICKET', CharField()))

    reviews = Review.objects.filter(user=user).annotate(type=Value('REVIEW', CharField()))

    posts = sorted(chain(reviews, tickets),
                    key=lambda post: post.time_created,
                    reverse=True)

    for ticket in tickets:
        print(ticket.type)
                    
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
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
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
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
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


def review(request, review_id):
    review = Review.objects.get(id=review_id)
    return render(request,
                "Webapp/review.html",
                {
                    "review": review,
                    "ticket": review.ticket,
                })


def review_create(request, related_ticket_id=None):
    if related_ticket_id:
        ticket = related_ticket_id

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() & review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("review-profil", review.id)

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request,
                "Webapp/review_create.html",
                {
                    "ticket": ticket,
                    "ticket_form": ticket_form,
                    "review_form": review_form
                })


def review_change(request):
    return


def review_delete(request):
    return


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


# user__followed_user