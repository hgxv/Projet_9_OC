from django.forms import CharField
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Webapp.forms import TicketForm, ReviewForm
from Webapp.models import Ticket, Review, UserFollow
from django.db.models import CharField, Value
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from itertools import chain


@login_required
def index(request):
    user = request.user
    request_followed = UserFollow.objects.filter(user=user)
    followed = [user]
    for people in request_followed:
        followed.append(people.followed_user)

    print(followed)
    
    tickets = Ticket.objects.filter(user__in=followed).annotate(type=Value('TICKET', CharField()))
    reviews = Review.objects.filter(
                            Q(user__in=followed) | Q(ticket__user=user)
                            ).annotate(type=Value('REVIEW', CharField()))

    posts = sorted(chain(reviews, tickets),
                    key=lambda post: post.time_created,
                    reverse=True)

    return render(request,
            "Webapp/index.html",
            {"posts": posts})


def posts(request):
    user = request.user

    tickets = Ticket.objects.filter(user=user).annotate(type=Value('TICKET', CharField()))
    reviews = Review.objects.filter(user=user).annotate(type=Value('REVIEW', CharField()))

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
                {"review": review})


def review_create(request, ticket_id):

    if ticket_id != 0:
        ticket = Ticket.objects.get(id=ticket_id)
    
    else:
        ticket = None

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() & review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            if hasattr(ticket, 'user') == False:
                ticket.user = request.user
            ticket.has_response = True
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect("review-profil", review.id)

    else:
        ticket_form = TicketForm(instance=ticket)
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

    if request.method == "POST":
        to_follow = request.POST.get("username")
        follow = UserFollow()
        follow.user = user
        error = "aaaa"

        try:
            follow.followed_user = User.objects.get(username=to_follow)
            if to_follow == user.username:
                raise ValueError("Same Pseudo")

            follow.save()

        except ObjectDoesNotExist:
            error = "Cet utilisateur n'existe pas"

        except IntegrityError:
            error = "Vous suivez déjà cet utilisateur"

        except ValueError:
            error = "Vous ne pouvez pas vous suivre"       

    return render(request,
                "Webapp/follows.html",
                {
                    "user": user,
                    "follows": follows,
                    "followed": followed,
                    "error": error,
                })


def follow_delete(request, follow_id):
    follow = UserFollow.objects.get(id=follow_id)
    followed = follow.followed_user
    follow.delete()

    return render(request,
                "Webapp/follow_delete.html",
                {"followed": followed})
