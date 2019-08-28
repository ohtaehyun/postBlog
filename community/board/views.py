from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from comuUser.models import CommuUser

# Create your views here.


def index(request):
    if request.method == "POST":
        userName = request.POST.get('userName', None)
        userEmail = request.POST.get('userEmail', None)
        userPassword = request.POST.get('userPassword', None)
        err_msg = {}
        user = CommuUser
        if userName:
            user = CommuUser.objects.get(userName=userName)
        elif userEmail:
            user = CommuUser.objects.get(userEmail=userEmail)
        else:
            return render(request, 'index.html', err_msg)

        if check_password(userPassword, user.userPassword):
            request.session['user'] = user.id
            return render(request, "index.html")
        else:
            err_msg["error"] = "Wrong Password Dude!"
            return render(request, "index.html", err_msg)
    else:
        return render(request, 'index.html')
