from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import CommuUser
# Create your views here.


def signUp(request):
    if request.method == "POST":
        userName = request.POST.get('userName', None)
        userEmail = request.POST.get('userEmail', None)
        userPassword = request.POST.get('userPassword', None)
        userPasswordCheck = request.POST.get('userPasswordCheck', None)
        err_msg = {}
        if not(userName and userEmail and userPassword and userPasswordCheck):
            err_msg['error'] = "모든 값을 입력하십쇼 HUMAN"

        elif(userPassword != userPasswordCheck):
            err_msg['error'] = "비밀번호가 서로 다릅니다!!!!!!!!!"
        else:
            commuUser = CommuUser(
                userName=userName,
                userEmail=userEmail,
                userPassword=make_password(userPassword)
            )
            commuUser.save()
            return redirect("../../")
        return render(request, "signUp.html", err_msg)

    else:
        return render(request, "signUp.html")
