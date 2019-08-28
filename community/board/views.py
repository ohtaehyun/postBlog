from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from comuUser.models import CommuUser

# Create your views here.


def review(request):
    return render(request, "review.html")


def study(request):
    return render(request, "study.html")


def home(request):
    msg = {}
    if request.session.session_key is not None:
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    else:
        msg['name'] = "unidentified"

    return render(request, "home.html", msg)


def signIn(request):
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
            return render(request, 'signIn.html', err_msg)

        if check_password(userPassword, user.userPassword):
            request.session['user'] = user.id
            request.session['name'] = user.userName
            return redirect("/home")
        else:
            err_msg["error"] = "Wrong Password Dude!"
            return render(request, "signIn.html", err_msg)
    else:
        return render(request, 'signIn.html')
