from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from comuUser.models import CommuUser

# Create your views here.


def signOut(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('../')


def review(request):
    msg = {}
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    return render(request, "review.html", msg)


def study(request):
    msg = {}

    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    return render(request, "study.html", msg)


def home(request):
    msg = {}
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
    # else:
    #     msg['name'] = "unidentified"

    return render(request, "home.html", msg)


def signIn(request):
    if request.method == "POST":
        userName = request.POST.get('userName', None)
        userEmail = request.POST.get('userEmail', None)
        userPassword = request.POST.get('userPassword', None)
        err_msg = {}
        user = CommuUser
        if userName:
            user = get_object_or_404(CommuUser, userName=userName)
        elif userEmail:
            user = get_object_or_404(CommuUser, userEmail=userEmail)
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


# def error_404(request, ex):
#     data = {}
#     data['exception'] = 'exception'

#     return render(request, "404.html", data)
