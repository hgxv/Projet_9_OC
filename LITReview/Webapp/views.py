from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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
            "Registration/registered.html")
