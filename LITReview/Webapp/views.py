from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request,
                "Webapp/index.html")


def register(request):
    return render(request,
            "Registration/register.html")
