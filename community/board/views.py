from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from comuUser.models import CommuUser
from .models import post, category

# Create your views here.


def addPost(request):
    msg = {}
    if CommuUser.objects.get(id=request.session['user']) is None:
        return redirect('/')
    elif CommuUser.objects.get(id=request.session['user']).userName == "othdev95":
        msg['name'] = "othdev95"
        if request.method == "POST":
            #  make post model
            po = post(
                categoryId=category.objects.get(
                    categoryName=request.POST.get("categoryName")),
                postTitle=request.POST.get("postTitle"),
                postContent=request.POST.get("postContent"),
                author=CommuUser.objects.get(userName=msg['name'])
            )
            po.save()

            return redirect('/study')
        else:
            msg['cates'] = category.objects.all()
            return render(request, 'addPost.html', msg)

    else:
        return redirect('/')


def addCategory(request):
    msg = {}
    if CommuUser.objects.get(id=request.session['user']) is None:
        return redirect('/')
    elif CommuUser.objects.get(id=request.session['user']).userName == "othdev95":
        msg['name'] = "othdev95"
        if request.method == "POST":

            categoryName = request.POST.get("categoryName")

            if(categoryName is not None):
                cate = category(
                    categoryName=categoryName
                )
                cate.save()
                return redirect('/study')
            else:
                msg['error'] = "항목을 입력 하십쇼"
                return render(request, 'addCategory.html', msg)
        else:
            return render(request, 'addCategory.html', msg)
    else:
        return redirect('/')


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
    post_list = post.objects.all()
    cate_list = category.objects.all()
    print(post_list)
    print(cate_list)
    if request.session.get('user'):
        msg['msg'] = request.session['user']
        user = CommuUser.objects.get(id=request.session['user'])
        msg['name'] = user.userName
        print(user.userName)
    msg['cate_list'] = cate_list

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
