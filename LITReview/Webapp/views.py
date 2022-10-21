from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request,
                "Webapp/index.html")
    else:
        return redirect('login/')


def register(request):
    return render(request,
            "Registration/register.html")
